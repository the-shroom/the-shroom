
struct logAction {
  float value;
  String name;
};

struct ControlRelay {
  int pin;
  String name;
  float time;
};

enum opmode {
  manual,
  automatic
};
