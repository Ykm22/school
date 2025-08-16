using System;
using System.Runtime.InteropServices;

namespace rt
{
    public class Ellipsoid : Geometry
    {
        private Vector Center { get; }
        private Vector SemiAxesLength { get; }
        private double Radius { get; }
        
        
        public Ellipsoid(Vector center, Vector semiAxesLength, double radius, Material material, Color color) : base(material, color)
        {
            Center = center;
            SemiAxesLength = semiAxesLength;
            Radius = radius;
        }

        public Ellipsoid(Vector center, Vector semiAxesLength, double radius, Color color) : base(color)
        {
            Center = center;
            SemiAxesLength = semiAxesLength;
            Radius = radius;
        }

        public override Intersection GetIntersection(Line line, double minDist, double maxDist)
        {
            // TODO: ADD CODE HERE
            var A = Math.Pow(SemiAxesLength.ComponentsProduct(), 2) *
                (
                    (line.Dx / SemiAxesLength) *
                    (line.Dx / SemiAxesLength)
                );
            var B =
                2 * Math.Pow(SemiAxesLength.ComponentsProduct(), 2) *
                (
                    line.Dx
                        .Multiply(line.X0 - Center)
                        .Divide(
                            SemiAxesLength.Multiply(SemiAxesLength)
                        )
                        .ComponentsSum()
                );
            var C =
                Math.Pow(SemiAxesLength.ComponentsProduct(), 2) *
                (
                    (line.X0 - Center).Divide(SemiAxesLength) *
                    (line.X0 - Center).Divide(SemiAxesLength)
                    - Math.Pow(Radius, 2)
                );

            var delta = B * B - 4 * A * C;
            var valid = (delta >= 0);
            var visible = false;

            if(valid)
            {
                var t1 = (-B - Math.Sqrt(delta)) / (2 * A);
                var t2 = (-B + Math.Sqrt(delta)) / (2 * A);
                var t = t1;
                if(t1 <= minDist || ( t1 > minDist && t2 > minDist && t2 < t1))
                {
                    t = t2;
                }
                var Normal = new Vector();
                if(t > minDist && t < maxDist)
                {
                    visible = true;
                    var intersectionPoint = line.CoordinateToPosition(t);
                    Normal =
                        (
                            (intersectionPoint - Center)
                                .Divide(SemiAxesLength.Multiply(SemiAxesLength))
                        ) * 2.0;
                    Normal.Normalize();
                }
                return new Intersection(valid, visible, this, line, t, Normal);
            }

            return new Intersection();
        }
    }
}
