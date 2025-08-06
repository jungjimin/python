import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart'; // 데이터 저장을 위한 라이브러리
import 'dart:async'; // 타이머를 위한 라이브러리
import 'dart:convert'; // JSON 처리를 위한 라이브러리

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'To-Do List',
      theme: ThemeData(
        primarySwatch: Colors.indigo, // 기본 색상 설정
        fontFamily: 'NotoSansKR', // Noto Sans KR 폰트 사용 (pubspec.yaml에 설정 필요)
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: const TodoListScreen(),
    );
  }
}

class TodoListScreen extends StatefulWidget {
  const TodoListScreen({super.key});

  @override
  State<TodoListScreen> createState() => _TodoListScreenState();
}

class _TodoListScreenState extends State<TodoListScreen> {
  // 할 일 데이터를 저장할 맵 (카테고리별 리스트)
  Map<String, List<Map<String, dynamic>>> todos = {
    "반영": [],
    "문의": [],
    "기타": [],
  };

  // 각 카테고리의 입력 컨트롤러
  final Map<String, TextEditingController> _controllers = {
    "반영": TextEditingController(),
    "문의": TextEditingController(),
    "기타": TextEditingController(),
  };

  // 알림 타이머를 관리할 맵
  final Map<String, Timer> _alarmTimers = {};

  @override
  void initState() {
    super.initState();
    _loadTodos(); // 앱 시작 시 저장된 할 일 로드
  }

  @override
  void dispose() {
    _controllers.forEach((key, controller) => controller.dispose()); // 컨트롤러 해제
    _alarmTimers.forEach((key, timer) => timer.cancel()); // 모든 타이머 해제
    super.dispose();
  }

  // 할 일 데이터 로드
  Future<void> _loadTodos() async {
    final prefs = await SharedPreferences.getInstance();
    final String? todosJson = prefs.getString('todos_db');
    if (todosJson != null) {
      setState(() {
        todos = Map<String, List<Map<String, dynamic>>>.from(
          (json.decode(todosJson) as Map).map((key, value) => MapEntry(
                key,
                (value as List)
                    .map((item) => Map<String, dynamic>.from(item))
                    .toList(),
              )),
        );
      });
      _startAllAlarms(); // 로드된 할 일 중 알람 설정된 것들 시작
    }
  }

  // 할 일 데이터 저장
  Future<void> _saveTodos() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('todos_db', json.encode(todos));
  }

  // 모든 알람 시작 (앱 로드 시)
  void _startAllAlarms() {
    todos.forEach((category, todoList) {
      for (int i = 0; i < todoList.length; i++) {
        final todoItem = todoList[i];
        if (todoItem['alarmTime'] != null && !todoItem['completed']) {
          _scheduleAlarm(
            todoItem['id'],
            todoItem['text'],
            DateTime.parse(todoItem['alarmTime']),
            category,
          );
        }
      }
    });
  }

  // 할 일 추가
  void _addTodo(String category, TextEditingController controller) {
    final text = controller.text.trim();
    if (text.isEmpty) return;

    setState(() {
      todos[category]!.insert(0, {
        'id': DateTime.now().millisecondsSinceEpoch.toString(), // 고유 ID
        'text': text,
        'completed': false,
        'alarmTime': null,
      });
    });
    _saveTodos();
    controller.clear();
  }

  // 할 일 완료/미완료 토글
  void _toggleComplete(String category, String id) {
    setState(() {
      final index = todos[category]!.indexWhere((item) => item['id'] == id);
      if (index != -1) {
        todos[category]![index]['completed'] = true;
        todos[category]![index]['alarmTime'] = null; // 완료 시 알람 취소
        _cancelAlarm(id); // 타이머 취소
      }
    });
    _saveTodos();
  }

  // 할 일 삭제
  void _deleteTodo(String category, String id) {
    setState(() {
      todos[category]!.removeWhere((item) => item['id'] == id);
      _cancelAlarm(id); // 타이머 취소
    });
    _saveTodos();
  }

  // 알람 취소 헬퍼
  void _cancelAlarm(String id) {
    if (_alarmTimers.containsKey(id)) {
      _alarmTimers[id]!.cancel();
      _alarmTimers.remove(id);
    }
  }

  // 알람 설정 옵션 표시
  void _showAlarmOptions(String category, String id) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: const Text("알림 시간 선택"),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: <Widget>[
              _buildAlarmOptionButton("5초 뒤", 5, category, id),
              _buildAlarmOptionButton("30분 뒤", 30 * 60, category, id),
              _buildAlarmOptionButton("1시간 뒤", 60 * 60, category, id),
            ],
          ),
        );
      },
    );
  }

  // 알람 옵션 버튼 빌더
  Widget _buildAlarmOptionButton(
      String text, int seconds, String category, String id) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4.0),
      child: ElevatedButton(
        onPressed: () {
          Navigator.of(context).pop(); // 다이얼로그 닫기
          _setAlarm(category, id, seconds);
        },
        style: ElevatedButton.styleFrom(
          minimumSize: const Size.fromHeight(40), // 버튼 높이 설정
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8),
          ),
          backgroundColor: Colors.indigo[400], // 버튼 배경색
          foregroundColor: Colors.white, // 버튼 글자색
          textStyle: const TextStyle(fontSize: 14, fontWeight: FontWeight.bold),
        ),
        child: Text(text),
      ),
    );
  }

  // 알람 설정
  void _setAlarm(String category, String id, int seconds) {
    setState(() {
      final index = todos[category]!.indexWhere((item) => item['id'] == id);
      if (index != -1) {
        final alarmTime = DateTime.now().add(Duration(seconds: seconds));
        todos[category]![index]['alarmTime'] = alarmTime.toIso8601String();
        _scheduleAlarm(id, todos[category]![index]['text'], alarmTime, category);
      }
    });
    _saveTodos();
  }

  // 알람 스케줄링
  void _scheduleAlarm(
      String id, String taskText, DateTime alarmTime, String category) {
    _cancelAlarm(id); // 기존 타이머가 있다면 취소

    final Duration timeUntilAlarm = alarmTime.difference(DateTime.now());

    if (timeUntilAlarm.inMilliseconds <= 1000) {
      // 1초 이내면 바로 알림 표시
      _showNotification(taskText);
      setState(() {
        final index = todos[category]!.indexWhere((item) => item['id'] == id);
        if (index != -1) {
          todos[category]![index]['alarmTime'] = null; // 알림 후 알람 시간 초기화
        }
      });
      _saveTodos();
      return;
    }

    _alarmTimers[id] = Timer.periodic(const Duration(seconds: 1), (timer) {
      final remaining = alarmTime.difference(DateTime.now());
      if (remaining.inSeconds <= 0) {
        _showNotification(taskText);
        setState(() {
          final index = todos[category]!.indexWhere((item) => item['id'] == id);
          if (index != -1) {
            todos[category]![index]['alarmTime'] = null; // 알림 후 알람 시간 초기화
          }
        });
        _saveTodos();
        timer.cancel();
        _alarmTimers.remove(id);
      }
      // UI 업데이트를 위해 setState 호출
      setState(() {
        // 이 setState는 UI를 직접 업데이트하지 않고, rebuild를 트리거하여
        // _buildTodoItem 위젯 내부의 타이머 텍스트가 갱신되도록 합니다.
      });
    });
  }

  // 알림 팝업 표시
  void _showNotification(String message) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          backgroundColor: Colors.indigo, // 알림 배경색
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Icon(Icons.notifications_active, color: Colors.white, size: 40),
              const SizedBox(height: 10),
              Text(
                "🚨 알림: $message",
                style: const TextStyle(color: Colors.white, fontSize: 16),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: () {
                  Navigator.of(context).pop();
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.white, // 닫기 버튼 배경색
                  foregroundColor: Colors.indigo, // 닫기 버튼 글자색
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                ),
                child: const Text("확인"),
              ),
            ],
          ),
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF8F9FA), // 배경색
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: <Widget>[
            // 앱 제목
            const Text(
              'To-Do List 📝',
              textAlign: TextAlign.center,
              style: TextStyle(
                color: Color(0xFF5C6BC0), // primary-color
                fontWeight: FontWeight.bold,
                fontSize: 24.0,
              ),
            ),
            const SizedBox(height: 20.0),

            // 각 카테고리 섹션
            ...todos.keys.map((category) {
              return _buildCategorySection(category);
            }).toList(),
          ],
        ),
      ),
    );
  }

  // 카테고리 섹션 빌더
  Widget _buildCategorySection(String category) {
    return Container(
      margin: const EdgeInsets.only(bottom: 20.0),
      padding: const EdgeInsets.all(15.0),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12.0),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.08),
            spreadRadius: 0,
            blurRadius: 12,
            offset: const Offset(0, 4), // changes position of shadow
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: <Widget>[
          // 카테고리 제목
          Container(
            padding: const EdgeInsets.only(bottom: 8.0),
            decoration: const BoxDecoration(
              border: Border(
                bottom: BorderSide(
                  color: Color(0xFFE0E0E0), // border-color
                  width: 2.0,
                ),
              ),
            ),
            child: Text(
              category,
              style: const TextStyle(
                color: Color(0xFF5C6BC0), // primary-color
                fontWeight: FontWeight.bold,
                fontSize: 18.0,
              ),
            ),
          ),
          const SizedBox(height: 12.0),

          // 할 일 입력 필드 및 추가 버튼
          Row(
            children: <Widget>[
              Expanded(
                child: TextField(
                  controller: _controllers[category],
                  decoration: InputDecoration(
                    hintText: '할 일 입력',
                    hintStyle: const TextStyle(fontSize: 12),
                    contentPadding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(8.0),
                      borderSide: const BorderSide(color: Color(0xFFE0E0E0)),
                    ),
                    enabledBorder: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(8.0),
                      borderSide: const BorderSide(color: Color(0xFFE0E0E0)),
                    ),
                    focusedBorder: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(8.0),
                      borderSide: const BorderSide(color: Color(0xFF5C6BC0)), // primary-color
                    ),
                  ),
                  style: const TextStyle(fontSize: 12),
                  onSubmitted: (_) => _addTodo(category, _controllers[category]!),
                ),
              ),
              const SizedBox(width: 10.0),
              SizedBox(
                width: 46, // 버튼 너비 고정
                height: 46, // 버튼 높이 고정
                child: ElevatedButton(
                  onPressed: () => _addTodo(category, _controllers[category]!),
                  style: ElevatedButton.styleFrom(
                    padding: EdgeInsets.zero, // 패딩 제거
                    backgroundColor: const Color(0xFF5C6BC0), // primary-color
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(8.0),
                    ),
                    elevation: 0, // 그림자 제거
                  ),
                  child: const Icon(Icons.add, color: Colors.white, size: 24), // ➕ 아이콘
                ),
              ),
            ],
          ),
          const SizedBox(height: 15.0),

          // 할 일 목록
          ListView.builder(
            shrinkWrap: true, // 부모 Column에 맞춰 크기 조절
            physics: const NeverScrollableScrollPhysics(), // 내부 스크롤 비활성화
            itemCount: todos[category]!.length,
            itemBuilder: (context, index) {
              final todoItem = todos[category]![index];
              final String id = todoItem['id'];
              final String text = todoItem['text'];
              final bool completed = todoItem['completed'];
              final String? alarmTimeStr = todoItem['alarmTime'];

              DateTime? alarmTime;
              if (alarmTimeStr != null) {
                alarmTime = DateTime.tryParse(alarmTimeStr);
              }

              // 각 할 일 항목 위젯 빌드
              return _buildTodoItem(
                id,
                text,
                completed,
                alarmTime,
                category,
              );
            },
          ),
        ],
      ),
    );
  }

  // 개별 할 일 항목 위젯 빌더
  Widget _buildTodoItem(
    String id,
    String text,
    bool completed,
    DateTime? alarmTime,
    String category,
  ) {
    // 알람 타이머 텍스트 계산
    String? alarmTimerText;
    if (alarmTime != null && !completed) {
      final remaining = alarmTime.difference(DateTime.now());
      if (remaining.inSeconds > 0) {
        final minutes = remaining.inMinutes;
        final seconds = remaining.inSeconds % 60;
        alarmTimerText = minutes > 0 ? '$minutes분 $seconds초' : '$seconds초';
      } else {
        alarmTimerText = '0초'; // 이미 지난 시간
      }
    }

    return Container(
      margin: const EdgeInsets.only(bottom: 8.0),
      padding: const EdgeInsets.symmetric(horizontal: 15, vertical: 10),
      decoration: BoxDecoration(
        color: const Color(0xFFF8F9FA), // 할 일 항목 배경색
        borderRadius: BorderRadius.circular(8.0),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.05),
            spreadRadius: 0,
            blurRadius: 4,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Row(
        children: <Widget>[
          Expanded(
            child: Text(
              text,
              style: TextStyle(
                fontSize: 12.0,
                decoration: completed ? TextDecoration.lineThrough : null,
                color: completed ? const Color(0xFF868E96) : const Color(0xFF343A40),
              ),
            ),
          ),
          const SizedBox(width: 5.0), // 텍스트와 버튼 사이 간격

          // 알람 타이머 또는 알람 버튼
          if (alarmTimerText != null && !completed)
            Text(
              alarmTimerText,
              style: const TextStyle(
                fontSize: 12.0,
                fontWeight: FontWeight.bold,
                color: Color(0xFFFFC107), // alarm-color
              ),
            )
          else if (!completed)
            IconButton(
              icon: const Icon(Icons.alarm, color: Color(0xFFFFC107)),
              onPressed: () => _showAlarmOptions(category, id),
              iconSize: 20, // 아이콘 크기
              padding: EdgeInsets.zero, // 패딩 제거
              constraints: const BoxConstraints(), // 최소 크기 제약 해제
            ),

          // 완료 버튼
          IconButton(
            icon: const Icon(Icons.check_circle, color: Color(0xFF4CAF50)),
            onPressed: () => _toggleComplete(category, id),
            iconSize: 20,
            padding: EdgeInsets.zero,
            constraints: const BoxConstraints(),
            color: completed ? Colors.transparent : null, // 완료 시 투명하게
          ),

          // 삭제 버튼
          IconButton(
            icon: const Icon(Icons.delete, color: Color(0xFFFF5252)),
            onPressed: () => _deleteTodo(category, id),
            iconSize: 20,
            padding: EdgeInsets.zero,
            constraints: const BoxConstraints(),
          ),
        ],
      ),
    );
  }
}
