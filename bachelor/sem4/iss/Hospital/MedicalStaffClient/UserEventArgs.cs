using System;
using System.Collections.Generic;

namespace Hospital
{
    public enum UserEvent
    {
        Update_AddedMedicine,
        Update_UpdatedMedicine,
        Update_DeletedMedicine,
        Update_UpdatedOrder,
        Update_AddedOrder
    };
    public class UserEventArgs : EventArgs
    {
        private readonly UserEvent userEvent;
        private readonly object data;

        public UserEventArgs(UserEvent userEvent, object data)
        {
            this.userEvent = userEvent;
            this.data = data;
        }

        public UserEvent UserEventType
        {
            get { return userEvent; }
        }

        public virtual object Data
        {
            get
            {
                return data;
            }
        }
    }
}