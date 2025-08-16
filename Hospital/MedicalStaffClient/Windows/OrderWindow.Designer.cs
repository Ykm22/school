using System.ComponentModel;

namespace MedicalStaffClient
{
    partial class OrderWindow
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
            this.button_Send = new System.Windows.Forms.Button();
            this.label2 = new System.Windows.Forms.Label();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridView_Medicines)).BeginInit();
            this.SuspendLayout();
            // 
            // dataGridView_Medicines
            // 
            this.dataGridView_Medicines.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dataGridView_Medicines.Location = new System.Drawing.Point(59, 84);
            this.dataGridView_Medicines.Name = "dataGridView_Medicines";
            this.dataGridView_Medicines.RowTemplate.Height = 24;
            this.dataGridView_Medicines.Size = new System.Drawing.Size(538, 232);
            this.dataGridView_Medicines.TabIndex = 0;
            // 
            // label1
            // 
            this.label1.Location = new System.Drawing.Point(290, 45);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(73, 20);
            this.label1.TabIndex = 1;
            this.label1.Text = "Medicines";
            // 
            // button_Send
            // 
            this.button_Send.Location = new System.Drawing.Point(275, 333);
            this.button_Send.Name = "button_Send";
            this.button_Send.Size = new System.Drawing.Size(88, 31);
            this.button_Send.TabIndex = 2;
            this.button_Send.Text = "Send";
            this.button_Send.UseVisualStyleBackColor = true;
            this.button_Send.Click += new System.EventHandler(this.button_Send_Click);
            // 
            // label2
            // 
            this.label2.Location = new System.Drawing.Point(24, 18);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(234, 22);
            this.label2.TabIndex = 3;
            this.label2.Text = "Select medicines from main window";
            // 
            // OrderWindow
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(667, 392);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.button_Send);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.dataGridView_Medicines);
            this.Name = "OrderWindow";
            this.Text = "OrderWindow";
            ((System.ComponentModel.ISupportInitialize)(this.dataGridView_Medicines)).EndInit();
            this.ResumeLayout(false);
        }

        private System.Windows.Forms.Label label2;

        private System.Windows.Forms.DataGridView dataGridView_Medicines;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Button button_Send;

        #endregion
    }
}