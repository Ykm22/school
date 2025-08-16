﻿using System.ComponentModel;

namespace client
{
    partial class OrderMedicinesWindow
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
            this.button_Complete = new System.Windows.Forms.Button();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridView_Medicines)).BeginInit();
            this.SuspendLayout();
            // 
            // label1
            // 
            this.label1.Location = new System.Drawing.Point(325, 49);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(100, 23);
            this.label1.TabIndex = 0;
            this.label1.Text = "Medicines";
            // 
            // dataGridView_Medicines
            // 
            this.dataGridView_Medicines.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dataGridView_Medicines.Location = new System.Drawing.Point(85, 104);
            this.dataGridView_Medicines.Name = "dataGridView_Medicines";
            this.dataGridView_Medicines.RowTemplate.Height = 24;
            this.dataGridView_Medicines.Size = new System.Drawing.Size(607, 267);
            this.dataGridView_Medicines.TabIndex = 1;
            // 
            // button_Complete
            // 
            this.button_Complete.Location = new System.Drawing.Point(325, 398);
            this.button_Complete.Name = "button_Complete";
            this.button_Complete.Size = new System.Drawing.Size(75, 29);
            this.button_Complete.TabIndex = 2;
            this.button_Complete.Text = "Complete";
            this.button_Complete.UseVisualStyleBackColor = true;
            this.button_Complete.Click += new System.EventHandler(this.button_Complete_Click);
            // 
            // OrderMedicinesWindow
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(800, 450);
            this.Controls.Add(this.button_Complete);
            this.Controls.Add(this.dataGridView_Medicines);
            this.Controls.Add(this.label1);
            this.Name = "OrderMedicinesWindow";
            this.Text = "OrderMedicinesWindow";
            ((System.ComponentModel.ISupportInitialize)(this.dataGridView_Medicines)).EndInit();
            this.ResumeLayout(false);
        }

        private System.Windows.Forms.Button button_Complete;

        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.DataGridView dataGridView_Medicines;

        #endregion
    }
}