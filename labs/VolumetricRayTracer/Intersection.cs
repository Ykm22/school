namespace rt
{
    public class Intersection
    {
        public static readonly Intersection NONE = new();

        public bool Valid { get; set; }
        public bool Visible { get; set; }
        public double T { get; }
        public Vector Position { get; }
        public Geometry Geometry { get; set; }
        public Line Line { get; }

        public Vector Normal { get; }
        public Material Material { get; set; }
        public Color Color { get; set; }

        public Intersection()
        {
            Geometry = null;
            Line = null;
            Valid = false;
            Visible = false;
            T = 0;
            Position = null;
            Normal = null;
            Material = new();
            Color = new();
        }

        public Intersection(double minDist, double maxDist, Line line, double t, Vector normal)
        {
            Line = line;
            Valid = true;
            T = t;
            Position = Line.CoordinateToPosition(t);
            Visible = T >= minDist && T <= maxDist;
            Normal = normal;
        }

        public Intersection(double minDist, double maxDist, Geometry geometry, Line line, double t, Vector normal, Material material, Color color)
        {
            Geometry = geometry;
            Line = line;
            Valid = true;
            T = t;
            Visible = T >= minDist && T <= maxDist;
            Position = Line.CoordinateToPosition(t);
            Normal = normal;
            Material = material;
            Color = color;
        }
    }
}