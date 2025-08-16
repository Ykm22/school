using System;
using System.Runtime.InteropServices;

namespace rt
{
    class RayTracer
    {
        private Geometry[] geometries;
        private Light[] lights;

        public RayTracer(Geometry[] geometries, Light[] lights)
        {
            this.geometries = geometries;
            this.lights = lights;
        }

        private double ImageToViewPlane(int n, int imgSize, double viewPlaneSize)
        {
            var u = n * viewPlaneSize / imgSize;
            u -= viewPlaneSize / 2;
            return u;
        }

        private Intersection FindFirstIntersection(Line ray, double minDist, double maxDist)
        {
            var intersection = new Intersection();

            foreach (var geometry in geometries)
            {
                var intr = geometry.GetIntersection(ray, minDist, maxDist);

                if (!intr.Valid || !intr.Visible) continue;

                if (!intersection.Valid || !intersection.Visible)
                {
                    intersection = intr;
                }
                else if (intr.T < intersection.T)
                {
                    intersection = intr;
                }
            }

            return intersection;
        }
        private double EuclidianDistance(Vector x, Vector y)
        {
            return Math.Sqrt(Math.Pow(y.X - x.X, 2) + Math.Pow(y.Y - x.Y, 2) + Math.Pow(y.Z - x.Z, 2));
        }

        private bool IsLit(Vector point, Light light)
        {
            // ADD CODE HERE: Detect whether the given point has a clear line of sight to the given light
            var ray = new Line(point, light.Position);
            var intersection = FindFirstIntersection(ray, 0, EuclidianDistance(point, light.Position));
            if(intersection.Valid && intersection.Visible)
            {
                return false;
            }
            return true;
        }

        public void Render(Camera camera, int width, int height, string filename)
        {
            var viewParallel = (camera.Up ^ camera.Direction).Normalize();

            var image = new Image(width, height);

            var vecW = camera.Direction * camera.ViewPlaneDistance;
            for (var i = 0; i < width; i++)
            {
                for (var j = 0; j < height; j++)
                {
                    var background = new Color(0, 0, 0, 1);
                    // ADD CODE HERE: Implement pixel color calculation
                    // Calculate x1 vector
                    var x1 = camera.Position + vecW +
                        camera.Up * ImageToViewPlane(j, height, camera.ViewPlaneHeight) +
                        viewParallel * ImageToViewPlane(i, width, camera.ViewPlaneWidth);

                    // My ray at this step
                    var ray = new Line(camera.Position, x1);

                    // First intersection between my ray and all objects
                    var firstIntersection = FindFirstIntersection(ray, camera.FrontPlaneDistance, camera.BackPlaneDistance);
                    var color = new Color();
                    if (firstIntersection.Valid && firstIntersection.Visible)
                    {
                        var intersectedMaterial = firstIntersection.Geometry.Material;

                        foreach(var light in lights)
                        {
                            // Ambient
                            color = intersectedMaterial.Ambient * light.Ambient; 
                            if(IsLit(firstIntersection.Position, light))
                            {
                                // Diffuse
                                var N = (firstIntersection.Position - firstIntersection.Geometry.GetCenter()).Normalize();
                                var T = (light.Position - firstIntersection.Position).Normalize();
                                if (N * T > 0)
                                {
                                    color += intersectedMaterial.Diffuse * light.Diffuse * (N * T);
                                }
                                // Specular
                                var E = (camera.Position - firstIntersection.Position).Normalize();
                                var R = ((N ^ T) ^ N * 2 - T).Normalize();
                                if (E * R > 0)
                                {
                                    color += intersectedMaterial.Specular * light.Specular * Math.Pow(E * R, intersectedMaterial.Shininess);
                                }
                            }
                            color *= light.Intensity;
                            background = new Color(
                                Math.Clamp(background.Red + color.Red, 0, 1),
                                Math.Clamp(background.Green + color.Green, 0, 1),
                                Math.Clamp(background.Blue + color.Blue, 0, 1),
                                Math.Clamp(background.Alpha + color.Alpha, 0, 1)
                            );
                        }

                    }
                    
                    image.SetPixel(i, j, background);
                }
            }

            image.Store(filename);
        }
    }
}