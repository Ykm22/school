using System.ComponentModel;

namespace MedicalStaffClient
{
    partial class LoginMedicalStaffWindow
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
            this.button_Login = new System.Windows.Forms.Button();
            this.textBox_Name = new System.Windows.Forms.TextBox();
            this.label2 = new System.Windows.Forms.Label();
            this.label1 = new System.Windows.Forms.Label();
            this.textBox_Password = new System.Windows.Forms.TextBox();
            this.SuspendLayout();
            // 
            // button_Login
            // 
            this.button_Login.Location = new System.Drawing.Point(43, 112);
            this.button_Login.Name = "button_Login";
            this.button_Login.Size = new System.Drawing.Size(204, 26);
            this.button_Login.TabIndex = 9;
            this.button_Login.Text = "Login";
            this.button_Login.UseVisualStyleBackColor = true;
            this.button_Login.Click += new System.EventHandler(this.button_Login_Click);
            // 
            // textBox_Name
            // 
            this.textBox_Name.Location = new System.Drawing.Point(124, 47);
            this.textBox_Name.Name = "textBox_Name";
            this.textBox_Name.Size = new System.Drawing.Size(123, 22);
            this.textBox_Name.TabIndex = 7;
            // 
            // label2
            // 
            this.label2.Location = new System.Drawing.Point(44, 74);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(74, 23);
            this.label2.TabIndex = 6;
            this.label2.Text = "Password:";
            // 
            // label1
            // 
            this.label1.Location = new System.Drawing.Point(44, 46);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(74, 23);
            this.label1.TabIndex = 5;
            this.label1.Text = "Name: ";
            // 
            // textBox_Password
            // 
            this.textBox_Password.Location = new System.Drawing.Point(124, 75);
            this.textBox_Password.Name = "textBox_Password";
            this.textBox_Password.Size = new System.Drawing.Size(123, 22);
            this.textBox_Password.TabIndex = 10;
            // 
            // LoginMedicalStaffWindow
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(288, 167);
            this.Controls.Add(this.textBox_Password);
            this.Controls.Add(this.button_Login);
            this.Controls.Add(this.textBox_Name);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.label1);
            this.Name = "LoginMedicalStaffWindow";
            this.Text = "LoginMedicalStaffWindow";
            this.ResumeLayout(false);
            this.PerformLayout();
        }

        private System.Windows.Forms.TextBox textBox_Password;

        private System.Windows.Forms.Button button_Login;
        private System.Windows.Forms.TextBox textBox_Name;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label label1;

        #endregion
    }
}