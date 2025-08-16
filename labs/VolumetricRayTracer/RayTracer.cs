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

        private bool IsLit(Vector point, Light light)
        {
            // ADD CODE HERE: Detect whether the given point has a clear line of sight to the given light
            var ray = new Line(point, light.Position);
            var intersection = FindFirstIntersection(ray, 0.001, 1e9);
            if (intersection.Valid && intersection.Visible)
            {
                return false;
            }
            return true;
        }

        public void Render(Camera camera, int width, int height, string filename)
        {
            var image = new Image(width, height);

            var vecW = camera.Direction * camera.ViewPlaneDistance;
            var viewParallel = (camera.Up ^ camera.Direction).Normalize();

            for (var i = 0; i < width; i++)
            {
                for (var j = 0; j < height; j++)
                {
                    var background = new Color(0, 0, 0, 1);

                    // Calculate x1 vector
                    var x1 = camera.Position + vecW +
                            camera.Up * ImageToViewPlane(j, height, camera.ViewPlaneHeight) +
                            viewParallel * ImageToViewPlane(i, width, camera.ViewPlaneWidth);

                    // My ray at this step
                    var ray = new Line(camera.Position, x1);

                    // First intersection between my ray and all objects
                    var intersection = FindFirstIntersection(ray, camera.FrontPlaneDistance, camera.BackPlaneDistance);
                    if (intersection.Valid && intersection.Visible)
                    {
                        var material = intersection.Material;

                        foreach (var light in lights)
                        {
                            var color = new Color();
                            // Ambient
                            color = material.Ambient * light.Ambient;

                            if (IsLit(intersection.Position, light))
                            {
                                // Diffuse
                                var N = intersection.Normal;
                                var T = (light.Position - intersection.Position).Normalize();
                                if (N * T > 0)
                                {
                                    color += material.Diffuse * light.Diffuse * (N * T);
                                }

                                // Specular
                                var E = (camera.Position - intersection.Position).Normalize();
                                var R = N * (N * T) * 2 - T;
                                if (E * R > 0)
                                {
                                    color += material.Specular * light.Specular * Math.Pow(E * R, material.Shininess);
                                }
                            }

                            // Intensity
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