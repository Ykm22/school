using System;
using System.Collections.Generic;

namespace client
{
    public enum UserEvent
    {
        Update_AddedMedicine,
        Update_UpdatedMedicine,
        Update_DeletedMedicine,
        Update_AddedOrder,
        Update_UpdatedOrder
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