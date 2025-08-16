using System.Collections.Generic;
using System.Linq;
using model;
using NHibernate;

namespace repository.MedicalStaffRepository
{
    public class DBMedicalStaffRepository : IMedicalStaffRepository<int, MedicalStaff>
    {
        public MedicalStaff Update(int id, MedicalStaff entity, bool substract)
        {
            throw new System.NotImplementedException();
        }

        private ISessionFactory _sessionFactory;
        public DBMedicalStaffRepository(ISessionFactory sessionFactory)
        {
            _sessionFactory = sessionFactory;
        }

        public MedicalStaff Save(MedicalStaff entity)
        {
            throw new System.NotImplementedException();
        }

        public MedicalStaff Delete(int id)
        {
            throw new System.NotImplementedException();
        }

        public IEnumerable<MedicalStaff> GetAll()
        {
            throw new System.NotImplementedException();
        }

        public MedicalStaff Find(int id)
        {
            throw new System.NotImplementedException();
        }

        public MedicalStaff Update(int id, MedicalStaff entity)
        {
            throw new System.NotImplementedException();
        }

        public MedicalStaff FindByCredentials(string medicalStaffName, string medicalStaffPassword)
        {
            using (var session = _sessionFactory.OpenSession())
            {
                var medicalStaff = session.Query<MedicalStaff>()
                    .FirstOrDefault(p => p.Name == medicalStaffName && p.Password == medicalStaffPassword);
                return medicalStaff;
            }
        }
    }
}