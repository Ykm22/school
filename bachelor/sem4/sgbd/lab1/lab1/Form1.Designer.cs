namespace lab1
{
    partial class Form1
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
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
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            dataGridView_SpatiiDeAnimale = new DataGridView();
            dataGridView_Animale = new DataGridView();
            buttonDelete = new Button();
            flowLayoutPanel_Update = new FlowLayoutPanel();
            ((System.ComponentModel.ISupportInitialize)dataGridView_SpatiiDeAnimale).BeginInit();
            ((System.ComponentModel.ISupportInitialize)dataGridView_Animale).BeginInit();
            SuspendLayout();
            // 
            // dataGridView_SpatiiDeAnimale
            // 
            dataGridView_SpatiiDeAnimale.ColumnHeadersHeightSizeMode = DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            dataGridView_SpatiiDeAnimale.Location = new Point(36, 23);
            dataGridView_SpatiiDeAnimale.Name = "dataGridView_SpatiiDeAnimale";
            dataGridView_SpatiiDeAnimale.RowHeadersWidth = 51;
            dataGridView_SpatiiDeAnimale.RowTemplate.Height = 29;
            dataGridView_SpatiiDeAnimale.Size = new Size(682, 185);
            dataGridView_SpatiiDeAnimale.TabIndex = 0;
            dataGridView_SpatiiDeAnimale.CellClick += dataGridView_SpatiiDeAnimale_CellClick;
            // 
            // dataGridView_Animale
            // 
            dataGridView_Animale.ColumnHeadersHeightSizeMode = DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            dataGridView_Animale.Location = new Point(36, 246);
            dataGridView_Animale.Name = "dataGridView_Animale";
            dataGridView_Animale.RowHeadersWidth = 51;
            dataGridView_Animale.RowTemplate.Height = 29;
            dataGridView_Animale.Size = new Size(682, 188);
            dataGridView_Animale.TabIndex = 1;
            dataGridView_Animale.CellClick += dataGridView_Animale_CellClick;
            // 
            // buttonDelete
            // 
            buttonDelete.Location = new Point(624, 449);
            buttonDelete.Name = "buttonDelete";
            buttonDelete.Size = new Size(94, 29);
            buttonDelete.TabIndex = 2;
            buttonDelete.Text = "Delete";
            buttonDelete.UseVisualStyleBackColor = true;
            buttonDelete.Click += buttonDelete_Click;
            // 
            // flowLayoutPanel_Update
            // 
            flowLayoutPanel_Update.Location = new Point(802, 19);
            flowLayoutPanel_Update.Name = "flowLayoutPanel_Update";
            flowLayoutPanel_Update.Size = new Size(250, 459);
            flowLayoutPanel_Update.TabIndex = 15;
            // 
            // Form1
            // 
            AutoScaleDimensions = new SizeF(8F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(1191, 546);
            Controls.Add(flowLayoutPanel_Update);
            Controls.Add(buttonDelete);
            Controls.Add(dataGridView_Animale);
            Controls.Add(dataGridView_SpatiiDeAnimale);
            Name = "Form1";
            Text = "Form1";
            Load += Form1_Load;
            ((System.ComponentModel.ISupportInitialize)dataGridView_SpatiiDeAnimale).EndInit();
            ((System.ComponentModel.ISupportInitialize)dataGridView_Animale).EndInit();
            ResumeLayout(false);
        }

        #endregion

        private DataGridView dataGridView_SpatiiDeAnimale;
        private DataGridView dataGridView_Animale;
        private Button buttonDelete;
        private FlowLayoutPanel flowLayoutPanel_Update;
    }
}