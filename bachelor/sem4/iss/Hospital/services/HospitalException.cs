using System;

namespace services
{
    public class HospitalException : Exception
    {
        public HospitalException() : base() {}
        public HospitalException(string msg) : base(msg) { }
        public HospitalException(string msg, Exception ex) : base(msg, ex) { }
    }
}