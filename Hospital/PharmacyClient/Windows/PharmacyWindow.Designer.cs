using System.ComponentModel;

namespace client
{
    partial class PharmacyWindow
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
            this.dataGridView_Medicines = new System.Windows.Forms.DataGridView();
            this.label1 = new System.Windows.Forms.Label();
            this.button_AddMedicine = new System.Windows.Forms.Button();
            this.button_DeleteMedicine = new System.Windows.Forms.Button();
            this.button_UpdateMedicine = new System.Windows.Forms.Button();
            this.button_FilterMedicines = new System.Windows.Forms.Button();
            this.button_Refresh = new System.Windows.Forms.Button();
            this.label2 = new System.Windows.Forms.Label();
            this.dataGridView_Orders = new System.Windows.Forms.DataGridView();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridView_Medicines)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridView_Orders)).BeginInit();
            this.SuspendLayout();
            // 
            // dataGridView_Medicines
            // 
            this.dataGridView_Medicines.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dataGridView_Medicines.Location = new System.Drawing.Point(34, 44);
            this.dataGridView_Medicines.Name = "dataGridView_Medicines";
            this.dataGridView_Medicines.RowTemplate.Height = 24;
            this.dataGridView_Medicines.Size = new System.Drawing.Size(586, 283);
            this.dataGridView_Medicines.TabIndex = 0;
            // 
            // label1
            // 
            this.label1.Location = new System.Drawing.Point(297, 9);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(73, 23);
            this.label1.TabIndex = 1;
            this.label1.Text = "Medicines";
            // 
            // button_AddMedicine
            // 
            this.button_AddMedicine.Location = new System.Drawing.Point(34, 338);
            this.button_AddMedicine.Name = "button_AddMedicine";
            this.button_AddMedicine.Size = new System.Drawing.Size(141, 38);
            this.button_AddMedicine.TabIndex = 2;
            this.button_AddMedicine.Text = "Add medicine";
            this.button_AddMedicine.UseVisualStyleBackColor = true;
            this.button_AddMedicine.Click += new System.EventHandler(this.button_AddMedicine_Click);
            // 
            // button_DeleteMedicine
            // 
            this.button_DeleteMedicine.Location = new System.Drawing.Point(479, 338);
            this.button_DeleteMedicine.Name = "button_DeleteMedicine";
            this.button_DeleteMedicine.Size = new System.Drawing.Size(141, 38);
            this.button_DeleteMedicine.TabIndex = 3;
            this.button_DeleteMedicine.Text = "Delete medicine";
            this.button_DeleteMedicine.UseVisualStyleBackColor = true;
            this.button_DeleteMedicine.Click += new System.EventHandler(this.button_DeleteMedicine_Click);
            // 
            // button_UpdateMedicine
            // 
            this.button_UpdateMedicine.Location = new System.Drawing.Point(34, 382);
            this.button_UpdateMedicine.Name = "button_UpdateMedicine";
            this.button_UpdateMedicine.Size = new System.Drawing.Size(141, 35);
            this.button_UpdateMedicine.TabIndex = 4;
            this.button_UpdateMedicine.Text = "Update medicine";
            this.button_UpdateMedicine.UseVisualStyleBackColor = true;
            this.button_UpdateMedicine.Click += new System.EventHandler(this.button_UpdateMedicine_Click);
            // 
            // button_FilterMedicines
            // 
            this.button_FilterMedicines.Location = new System.Drawing.Point(479, 382);
            this.button_FilterMedicines.Name = "button_FilterMedicines";
            this.button_FilterMedicines.Size = new System.Drawing.Size(141, 35);
            this.button_FilterMedicines.TabIndex = 5;
            this.button_FilterMedicines.Text = "Filter medicines";
            this.button_FilterMedicines.UseVisualStyleBackColor = true;
            this.button_FilterMedicines.Click += new System.EventHandler(this.button_FilterMedicines_Click);
            // 
            // button_Refresh
            // 
            this.button_Refresh.Location = new System.Drawing.Point(269, 338);
            this.button_Refresh.Name = "button_Refresh";
            this.button_Refresh.Size = new System.Drawing.Size(120, 79);
            this.button_Refresh.TabIndex = 6;
            this.button_Refresh.Text = "Refresh medicines";
            this.button_Refresh.UseVisualStyleBackColor = true;
            this.button_Refresh.Click += new System.EventHandler(this.button_Refresh_Click);
            // 
            // label2
            // 
            this.label2.Location = new System.Drawing.Point(297, 468);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(57, 23);
            this.label2.TabIndex = 7;
            this.label2.Text = "Orders";
            // 
            // dataGridView_Orders
            // 
            this.dataGridView_Orders.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dataGridView_Orders.Location = new System.Drawing.Point(123, 506);
            this.dataGridView_Orders.Name = "dataGridView_Orders";
            this.dataGridView_Orders.RowTemplate.Height = 24;
            this.dataGridView_Orders.Size = new System.Drawing.Size(416, 226);
            this.dataGridView_Orders.TabIndex = 8;
            this.dataGridView_Orders.CellClick += new System.Windows.Forms.DataGridViewCellEventHandler(this.dataGridView_Orders_CellClick);
            // 
            // PharmacyWindow
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(677, 768);
            this.Controls.Add(this.dataGridView_Orders);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.button_Refresh);
            this.Controls.Add(this.button_FilterMedicines);
            this.Controls.Add(this.button_UpdateMedicine);
            this.Controls.Add(this.button_DeleteMedicine);
            this.Controls.Add(this.button_AddMedicine);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.dataGridView_Medicines);
            this.Name = "PharmacyWindow";
            this.Text = "PharmacyWindow";
            ((System.ComponentModel.ISupportInitialize)(this.dataGridView_Medicines)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridView_Orders)).EndInit();
            this.ResumeLayout(false);
        }

        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.DataGridView dataGridView_Orders;

        private System.Windows.Forms.Button button_Refresh;

        private System.Windows.Forms.Button button_AddMedicine;
        private System.Windows.Forms.Button button_DeleteMedicine;
        private System.Windows.Forms.Button button_UpdateMedicine;
        private System.Windows.Forms.Button button_FilterMedicines;

        private System.Windows.Forms.DataGridView dataGridView_Medicines;
        private System.Windows.Forms.Label label1;

        #endregion
    }
}