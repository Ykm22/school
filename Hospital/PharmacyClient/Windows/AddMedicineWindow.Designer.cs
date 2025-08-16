using System.ComponentModel;

namespace client
{
    partial class AddMedicineWindow
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
            this.comboBox_Purpose = new System.Windows.Forms.ComboBox();
            this.label1 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.textBox_Name = new System.Windows.Forms.TextBox();
            this.label3 = new System.Windows.Forms.Label();
            this.numericUpDown_Quantity = new System.Windows.Forms.NumericUpDown();
            this.button_AddMedicine = new System.Windows.Forms.Button();
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDown_Quantity)).BeginInit();
            this.SuspendLayout();
            // 
            // comboBox_Purpose
            // 
            this.comboBox_Purpose.FormattingEnabled = true;
            this.comboBox_Purpose.Location = new System.Drawing.Point(106, 42);
            this.comboBox_Purpose.Name = "comboBox_Purpose";
            this.comboBox_Purpose.Size = new System.Drawing.Size(121, 24);
            this.comboBox_Purpose.TabIndex = 0;
            // 
            // label1
            // 
            this.label1.Location = new System.Drawing.Point(23, 45);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(68, 23);
            this.label1.TabIndex = 1;
            this.label1.Text = "Purpose:";
            // 
            // label2
            // 
            this.label2.Location = new System.Drawing.Point(23, 20);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(68, 23);
            this.label2.TabIndex = 2;
            this.label2.Text = "Name:";
            // 
            // textBox_Name
            // 
            this.textBox_Name.Location = new System.Drawing.Point(106, 14);
            this.textBox_Name.Name = "textBox_Name";
            this.textBox_Name.Size = new System.Drawing.Size(121, 22);
            this.textBox_Name.TabIndex = 3;
            // 
            // label3
            // 
            this.label3.Location = new System.Drawing.Point(23, 72);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(68, 24);
            this.label3.TabIndex = 4;
            this.label3.Text = "Quantity:";
            // 
            // numericUpDown_Quantity
            // 
            this.numericUpDown_Quantity.Location = new System.Drawing.Point(106, 72);
            this.numericUpDown_Quantity.Name = "numericUpDown_Quantity";
            this.numericUpDown_Quantity.Size = new System.Drawing.Size(121, 22);
            this.numericUpDown_Quantity.TabIndex = 5;
            // 
            // button_AddMedicine
            // 
            this.button_AddMedicine.Location = new System.Drawing.Point(23, 109);
            this.button_AddMedicine.Name = "button_AddMedicine";
            this.button_AddMedicine.Size = new System.Drawing.Size(204, 32);
            this.button_AddMedicine.TabIndex = 6;
            this.button_AddMedicine.Text = "Add";
            this.button_AddMedicine.UseVisualStyleBackColor = true;
            this.button_AddMedicine.Click += new System.EventHandler(this.button_AddMedicine_Click);
            // 
            // AddMedicineWindow
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(272, 176);
            this.Controls.Add(this.button_AddMedicine);
            this.Controls.Add(this.numericUpDown_Quantity);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.textBox_Name);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.comboBox_Purpose);
            this.Name = "AddMedicineWindow";
            this.Text = "AddMedicineWindow";
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDown_Quantity)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();
        }

        private System.Windows.Forms.ComboBox comboBox_Purpose;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.TextBox textBox_Name;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.NumericUpDown numericUpDown_Quantity;
        private System.Windows.Forms.Button button_AddMedicine;

        #endregion
    }
}