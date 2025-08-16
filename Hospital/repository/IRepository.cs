using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using model;

namespace repository
{
    public interface IRepository<in TId, TE> where TE : Identifiable
    {
        TE Save(TE entity);
        TE Delete(TId id);
        IEnumerable<TE> GetAll();
        TE Find(TId id);
        TE Update(TId id, TE entity);
        TE Update(TId id, TE entity, bool substract);
    }
}