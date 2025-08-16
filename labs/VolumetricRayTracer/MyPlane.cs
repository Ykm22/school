using System;
using System.Collections.Generic;
using System.Linq;
using System.Numerics;
using System.Security.Cryptography;
using System.Text;
using System.Threading.Tasks;

namespace rt
{
    public class MyPlane
    {
        public Vector X { get ;set; }
        public Vector Y { get ;set; }
        public double D { get ;set; }
        public Vector Normal { get; set; }
        public MyPlane() { }
        public static MyPlane PlaneFromPointsAndNormal(Vector x, Vector y, Vector Normal)
        {
            MyPlane plane = new();
            plane.X = x;
            plane.Y = y;
            plane.Normal = Normal;
            plane.D = -(Normal * x);

            return plane;
        }
        public Intersection GetIntersection(Line line, double minT, double maxT)
        {
            // Floating point check
            if (Math.Abs(line.Dx * Normal) <= 0.0001) return Intersection.NONE;
            double t = -(Normal * line.X0 + D) / (Normal * line.Dx);

            var S = Y - X;
            var P = line.CoordinateToPosition(t) - X;

            bool CheckFPComponents(double x1, double x2)
            {
                if (x1 <= 0.0001)
                {
                    return Math.Abs(x2) <= 0.0001;
                }
                else
                {
                    return x2 >= 0 && x2 <= x1;
                }
            }

            // Floating point checks
            if (!(CheckFPComponents(S.X, P.X) && CheckFPComponents(S.Y, P.Y) && CheckFPComponents(S.Z, P.Z)))
                return Intersection.NONE;
            return new Intersection(minT, maxT, line, t, Normal);
        }
    }
}
