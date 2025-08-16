using System.ComponentModel;

namespace client
{
    partial class DeleteMedicineWindow
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
            this.numericUpDown_IdDelete = new System.Windows.Forms.NumericUpDown();
            this.button_Delete = new System.Windows.Forms.Button();
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDown_IdDelete)).BeginInit();
            this.SuspendLayout();
            // 
            // label1
            // 
            this.label1.Location = new System.Drawing.Point(12, 26);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(89, 22);
            this.label1.TabIndex = 0;
            this.label1.Text = "Id to delete:";
            // 
            // numericUpDown_IdDelete
            // 
            this.numericUpDown_IdDelete.Location = new System.Drawing.Point(107, 26);
            this.numericUpDown_IdDelete.Name = "numericUpDown_IdDelete";
            this.numericUpDown_IdDelete.Size = new System.Drawing.Size(120, 22);
            this.numericUpDown_IdDelete.TabIndex = 1;
            // 
            // button_Delete
            // 
            this.button_Delete.Location = new System.Drawing.Point(12, 62);
            this.button_Delete.Name = "button_Delete";
            this.button_Delete.Size = new System.Drawing.Size(215, 27);
            this.button_Delete.TabIndex = 2;
            this.button_Delete.Text = "Delete";
            this.button_Delete.UseVisualStyleBackColor = true;
            this.button_Delete.Click += new System.EventHandler(this.button_Delete_Click);
            // 
            // DeleteMedicineWindow
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(255, 109);
            this.Controls.Add(this.button_Delete);
            this.Controls.Add(this.numericUpDown_IdDelete);
            this.Controls.Add(this.label1);
            this.Name = "DeleteMedicineWindow";
            this.Text = "DeleteMedicineWindow";
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDown_IdDelete)).EndInit();
            this.ResumeLayout(false);
        }

        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.NumericUpDown numericUpDown_IdDelete;
        private System.Windows.Forms.Button button_Delete;

        #endregion
    }
}