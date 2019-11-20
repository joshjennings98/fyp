// Gmsh project created on Sat Aug 12 22:04:15 2017
//+
Point(3) = {4.6, -0.3, 0, 1.0};
//+
Point(4) = {2.3, 0.4, 0, 1.0};
//+
Point(5) = {3.8, 0.4, 0, 1.0};
//+
Point(6) = {3.8, -0.7, 0, 1.0};
//+
Point(7) = {2.3, -0.7, 0, 1.0};
//+
Line(1) = {4, 5};
//+
Line(2) = {5, 6};
//+
Line(3) = {6, 7};
//+
Line(4) = {7, 4};
//+
Line Loop(5) = {4, 1, 2, 3};
//+
Point(8) = {2.8, 0.1, 0, 1.0};
//+
Point(9) = {3, -0.1, 0, 1.0};
//+
Point(10) = {2.8, -0.3, 0, 1.0};
//+
Point(11) = {2.6, -0.1, 0, 1.0};
//+
Point(12) = {2.8, -0.1, 0, 1.0};
//+
Circle(6) = {8, 12, 8};
//+
Line Loop(7) = {6};
//+
Point(13) = {3.1, 0.2, 0, 1.0};
//+
Point(14) = {3.3, -0, 0, 1.0};
//+
Point(15) = {3.2, -0.2, 0, 1.0};
//+
Point(16) = {2.8, -0.5, 0, 1.0};
//+
Point(17) = {3.1, -0.6, 0, 1.0};
//+
Point(18) = {3.6, -0.6, 0, 1.0};
//+
Point(19) = {3.4, -0.4, 0, 1.0};
//+
Point(20) = {3.6, -0.2, 0, 1.0};
//+
Point(21) = {3.1, 0.3, 0, 1.0};
//+
Point(22) = {3.6, 0.1, 0, 1.0};
//+
Line(10) = {13, 14};
//+
Line(11) = {14, 22};
//+
Line(12) = {21, 22};
//+
Line(13) = {16, 15};
//+
Line(14) = {15, 20};
//+
Line(15) = {20, 18};
//+
Line(16) = {18, 17};
//+
Line(17) = {17, 16};
//+
Point(23) = {2.7, 0.3, 0, 1.0};
//+
Point(24) = {2.7, 0.2, 0, 1.0};
//+
Line(18) = {23, 21};
//+
Line(19) = {13, 24};
//+
Line(20) = {24, 23};
//+
Field[1] = Box;
//+
Field[1].VIn = 0.01;
//+
Field[1].VOut = 0.01;
//+
Mesh.SubdivisionAlgorithm=1;

//+
Line Loop(21) = {19, 20, 18, 12, -11, -10};
