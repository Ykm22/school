using System.ComponentModel;

namespace client
{
    partial class UpdateMedicineWindow
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
            this.asd = new System.Windows.Forms.Label();
            this.label1 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.numericUpDown_IdToUpdate = new System.Windows.Forms.NumericUpDown();
            this.textBox_NewName = new System.Windows.Forms.TextBox();
            this.comboBox_NewPurpose = new System.Windows.Forms.ComboBox();
            this.numericUpDown_NewQuantity = new System.Windows.Forms.NumericUpDown();
            this.button_Update = new System.Windows.Forms.Button();
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDown_IdToUpdate)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDown_NewQuantity)).BeginInit();
            this.SuspendLayout();
            // 
            // asd
            // 
            this.asd.Location = new System.Drawing.Point(31, 34);
            this.asd.Name = "asd";
            this.asd.Size = new System.Drawing.Size(90, 23);
            this.asd.TabIndex = 0;
            this.asd.Text = "Id to update:";
            // 
            // label1
            // 
            this.label1.Location = new System.Drawing.Point(31, 63);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(100, 23);
            this.label1.TabIndex = 1;
            this.label1.Text = "New name:";
            // 
            // label2
            // 
            this.label2.Location = new System.Drawing.Point(31, 94);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(100, 23);
            this.label2.TabIndex = 2;
            this.label2.Text = "New purpose:";
            // 
            // label3
            // 
            this.label3.Location = new System.Drawing.Point(31, 129);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(100, 23);
            this.label3.TabIndex = 3;
            this.label3.Text = "New quantity:";
            // 
            // numericUpDown_IdToUpdate
            // 
            this.numericUpDown_IdToUpdate.Location = new System.Drawing.Point(136, 32);
            this.numericUpDown_IdToUpdate.Name = "numericUpDown_IdToUpdate";
            this.numericUpDown_IdToUpdate.Size = new System.Drawing.Size(121, 22);
            this.numericUpDown_IdToUpdate.TabIndex = 4;
            // 
            // textBox_NewName
            // 
            this.textBox_NewName.Location = new System.Drawing.Point(136, 60);
            this.textBox_NewName.Name = "textBox_NewName";
            this.textBox_NewName.Size = new System.Drawing.Size(121, 22);
            this.textBox_NewName.TabIndex = 5;
            // 
            // comboBox_NewPurpose
            // 
            this.comboBox_NewPurpose.FormattingEnabled = true;
            this.comboBox_NewPurpose.Location = new System.Drawing.Point(136, 94);
            this.comboBox_NewPurpose.Name = "comboBox_NewPurpose";
            this.comboBox_NewPurpose.Size = new System.Drawing.Size(121, 24);
            this.comboBox_NewPurpose.TabIndex = 6;
            // 
            // numericUpDown_NewQuantity
            // 
            this.numericUpDown_NewQuantity.Location = new System.Drawing.Point(137, 127);
            this.numericUpDown_NewQuantity.Name = "numericUpDown_NewQuantity";
            this.numericUpDown_NewQuantity.Size = new System.Drawing.Size(120, 22);
            this.numericUpDown_NewQuantity.TabIndex = 7;
            // 
            // button_Update
            // 
            this.button_Update.Location = new System.Drawing.Point(31, 164);
            this.button_Update.Name = "button_Update";
            this.button_Update.Size = new System.Drawing.Size(226, 30);
            this.button_Update.TabIndex = 8;
            this.button_Update.Text = "Update";
            this.button_Update.UseVisualStyleBackColor = true;
            this.button_Update.Click += new System.EventHandler(this.button_Update_Click);
            // 
            // UpdateMedicineWindow
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(291, 222);
            this.Controls.Add(this.button_Update);
            this.Controls.Add(this.numericUpDown_NewQuantity);
            this.Controls.Add(this.comboBox_NewPurpose);
            this.Controls.Add(this.textBox_NewName);
            this.Controls.Add(this.numericUpDown_IdToUpdate);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.asd);
            this.Name = "UpdateMedicineWindow";
            this.Text = "UpdateMedicineWindow";
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDown_IdToUpdate)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDown_NewQuantity)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();
        }

        private System.Windows.Forms.Button button_Update;

        private System.Windows.Forms.NumericUpDown numericUpDown_IdToUpdate;
        private System.Windows.Forms.TextBox textBox_NewName;
        private System.Windows.Forms.ComboBox comboBox_NewPurpose;
        private System.Windows.Forms.NumericUpDown numericUpDown_NewQuantity;

        private System.Windows.Forms.Label asd;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label label3;

        #endregion
    }
}