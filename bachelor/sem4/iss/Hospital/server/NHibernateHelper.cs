using FluentNHibernate.Cfg;
using FluentNHibernate.Cfg.Db;
using model;
using NHibernate;

namespace server
{
    public class NHibernateHelper
    {
        private static ISessionFactory _sessionFactory;

        public static ISessionFactory SessionFactory
        {
            get
            {
                if (_sessionFactory == null)
                {
                    string connString = @"Data Source=D:\Facultate\anul_2\sem_2\ISS\Laborator\ISS-lab\Hospital\server\Hospital.db;Version=3";
                    _sessionFactory = Fluently.Configure()
                        .Database(SQLiteConfiguration.Standard.ConnectionString(connString))
                        .Mappings(m => m.FluentMappings.AddFromAssemblyOf<Pharmacist>())
                        .Mappings(m => m.FluentMappings.AddFromAssemblyOf<Medicine>())
                        .Mappings(m => m.FluentMappings.AddFromAssemblyOf<Order>())
                        .BuildSessionFactory();
                }

                return _sessionFactory;
            }
        }

        public static ISession GetSession()
        {
            return SessionFactory.OpenSession();
        }
    }
}