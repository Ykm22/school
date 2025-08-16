using System;

namespace rt
{
    public class Sphere : Geometry
    {
        public Vector Center { get; set; }
        public double Radius { get; set; }

        public Sphere(Vector center, double radius, Material material, Color color) : base(material, color)
        {
            Center = center;
            Radius = radius;
        }

        public override Intersection GetIntersection(Line line, double minDist, double maxDist)
        {
            // ADD CODE HERE: Calculate the intersection between the given line and this sphere
            var a = line.Dx.X;
            var c = line.Dx.Y;
            var e = line.Dx.Z;

            var b = line.X0.X; 
            var d = line.X0.Y;
            var f = line.X0.Z;

            var A = a * a + c * c + e * e;
            var B = 2 * (a * (b - Center.X) + c * (d - Center.Y) + e * (f - Center.Z));
            var C = (b - Center.X) * (b - Center.X) + (d - Center.Y) * (d - Center.Y) + (f - Center.Z) * (f - Center.Z) - Radius * Radius;

            var delta = B * B - 4 * A * C;

            var valid = (delta >= 0);
            var visible = false;

            if (valid)
            {
                var t1 = (-B - Math.Sqrt(delta)) / (2 * A);
                var t2 = (-B + Math.Sqrt(delta)) / (2 * A);

                var t = t1;
                if(t1 <= 0 || (t1 > 0 && t2 > 0 && t2 < t1 ))
                {
                    t = t2;
                }
                //var t = -1.0;
                //if(t1 > 0)
                //{
                //    t = t1;
                //}
                //else if (t2 > 0 && t2 < t1)
                //{
                //    t = t2;
                //} else
                //{
                //    visible = false;
                //}


                if(t > minDist && t < maxDist)
                {
                    visible = true;
                }
                return new Intersection(valid, visible, this, line, t);
            }
            return new Intersection();
        }

        public override Vector Normal(Vector v)
        {
            var n = v - Center;
            n.Normalize();
            return n;
        }
        public override Vector GetCenter()
        {
            return Center;
        }
    }
}