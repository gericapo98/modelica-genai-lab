within ;
model RC_Step
  import Modelica.Electrical.Analog.Basic.*;
  import Modelica.Electrical.Analog.Sources.*;
  import Modelica.Electrical.Analog.Ground;

  parameter Real R=1000 "Ohm";
  parameter Real C=1e-5 "F";

  Resistor     R1(R=R);
  Capacitor    C1(C=C, v(start=0));
  StepVoltage  V(stepHeight=1, startTime=0);
  Ground       G;

equation
  connect(V.p, R1.p);
  connect(R1.n, C1.p);
  connect(C1.n, V.n);
  connect(V.n, G.p);

annotation (experiment(StartTime=0, StopTime=1, Tolerance=1e-6, Interval=1e-3));
end RC_Step;
