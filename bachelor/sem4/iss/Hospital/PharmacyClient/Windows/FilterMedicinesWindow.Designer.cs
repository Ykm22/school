using System.ComponentModel;

namespace client
{
    partial class FilterMedicinesWindow
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
            this.comboBox_FilterPurpose = new System.Windows.Forms.ComboBox();
            this.button_Filter = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // label1
            // 
            this.label1.Location = new System.Drawing.Point(25, 22);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(127, 23);
            this.label1.TabIndex = 0;
            this.label1.Text = "Filtering purpose:";
            // 
            // comboBox_FilterPurpose
            // 
            this.comboBox_FilterPurpose.FormattingEnabled = true;
            this.comboBox_FilterPurpose.Location = new System.Drawing.Point(158, 22);
            this.comboBox_FilterPurpose.Name = "comboBox_FilterPurpose";
            this.comboBox_FilterPurpose.Size = new System.Drawing.Size(121, 24);
            this.comboBox_FilterPurpose.TabIndex = 1;
            // 
            // button_Filter
            // 
            this.button_Filter.Location = new System.Drawing.Point(25, 60);
            this.button_Filter.Name = "button_Filter";
            this.button_Filter.Size = new System.Drawing.Size(254, 30);
            this.button_Filter.TabIndex = 2;
            this.button_Filter.Text = "Filter";
            this.button_Filter.UseVisualStyleBackColor = true;
            this.button_Filter.Click += new System.EventHandler(this.button_Filter_Click);
            // 
            // FilterMedicinesWindow
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(319, 117);
            this.Controls.Add(this.button_Filter);
            this.Controls.Add(this.comboBox_FilterPurpose);
            this.Controls.Add(this.label1);
            this.Name = "FilterMedicinesWindow";
            this.Text = "FilterMedicinesWindow";
            this.ResumeLayout(false);
        }

        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.ComboBox comboBox_FilterPurpose;
        private System.Windows.Forms.Button button_Filter;

        #endregion
    }
}