using System.Collections.Generic;
using model;

namespace repository.MedicinesRepository
{
    public interface IMedicinesRepository<in TId, TE> : IRepository<TId, TE> where TE : Identifiable
    {
        IEnumerable<Medicine> FindByPurpose(Purpose purpose);
        IEnumerable<Medicine> FilterByOrderId(int orderId);
    }
}