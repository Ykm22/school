using System.ComponentModel;

namespace MedicalStaffClient
{
    partial class MedicalStaffWindow
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }

            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.label1 = new System.Windows.Forms.Label();
            this.dataGridView_Medicines = new System.Windows.Forms.DataGridView();
            this.button_NewOrder = new System.Windows.Forms.Button();
            this.Orders = new System.Windows.Forms.Label();
            this.dataGridView_Orders = new System.Windows.Forms.DataGridView();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridView_Medicines)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridView_Orders)).BeginInit();
            this.SuspendLayout();
            // 
            // label1
            // 
            this.label1.Location = new System.Drawing.Point(291, 20);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(75, 23);
            this.label1.TabIndex = 0;
            this.label1.Text = "Medicines";
            // 
            // dataGridView_Medicines
            // 
            this.dataGridView_Medicines.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dataGridView_Medicines.Location = new System.Drawing.Point(35, 62);
            this.dataGridView_Medicines.Name = "dataGridView_Medicines";
            this.dataGridView_Medicines.RowTemplate.Height = 24;
            this.dataGridView_Medicines.Size = new System.Drawing.Size(591, 283);
            this.dataGridView_Medicines.TabIndex = 1;
            this.dataGridView_Medicines.CellClick += new System.Windows.Forms.DataGridViewCellEventHandler(this.dataGridView_Medicines_CellClick);
            // 
            // button_NewOrder
            // 
            this.button_NewOrder.Location = new System.Drawing.Point(279, 362);
            this.button_NewOrder.Name = "button_NewOrder";
            this.button_NewOrder.Size = new System.Drawing.Size(97, 31);
            this.button_NewOrder.TabIndex = 2;
            this.button_NewOrder.Text = "New order";
            this.button_NewOrder.UseVisualStyleBackColor = true;
            this.button_NewOrder.Click += new System.EventHandler(this.button_NewOrder_Click);
            // 
            // Orders
            // 
            this.Orders.Location = new System.Drawing.Point(303, 420);
            this.Orders.Name = "Orders";
            this.Orders.Size = new System.Drawing.Size(63, 23);
            this.Orders.TabIndex = 3;
            this.Orders.Text = "Orders";
            // 
            // dataGridView_Orders
            // 
            this.dataGridView_Orders.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dataGridView_Orders.Location = new System.Drawing.Point(99, 466);
            this.dataGridView_Orders.Name = "dataGridView_Orders";
            this.dataGridView_Orders.RowTemplate.Height = 24;
            this.dataGridView_Orders.Size = new System.Drawing.Size(475, 198);
            this.dataGridView_Orders.TabIndex = 4;
            // 
            // MedicalStaffWindow
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(659, 694);
            this.Controls.Add(this.dataGridView_Orders);
            this.Controls.Add(this.Orders);
            this.Controls.Add(this.button_NewOrder);
            this.Controls.Add(this.dataGridView_Medicines);
            this.Controls.Add(this.label1);
            this.Name = "MedicalStaffWindow";
            this.Text = "MedicalStaffWindow";
            ((System.ComponentModel.ISupportInitialize)(this.dataGridView_Medicines)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridView_Orders)).EndInit();
            this.ResumeLayout(false);
        }

        private System.Windows.Forms.Label Orders;
        private System.Windows.Forms.DataGridView dataGridView_Orders;

        private System.Windows.Forms.Button button_NewOrder;

        private System.Windows.Forms.DataGridView dataGridView_Medicines;

        private System.Windows.Forms.Label label1;

        #endregion
    }
}