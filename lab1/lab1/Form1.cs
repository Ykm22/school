using Microsoft.Data.SqlClient;
using Microsoft.IdentityModel.Tokens;
using System.Data;

namespace lab1
{
    public partial class Form1 : Form
    {
        string connString;
        private int noParams;
        private string paramTypes;
        private string parentTable;
        private string childTable;
        DataSet ds = new DataSet();
        SqlDataAdapter adapter = new SqlDataAdapter();
        //for later use
        int cod_child = -1, cod_parent = -1;

        string selectParentCommand;
        string selectChildCommand;
        string deleteChildCommand;
        string updateChildCommand;
        string insertChildCommand;
        IDictionary<int, Tuple<TextBox, string>> textBoxes = new Dictionary<int, Tuple<TextBox, string>>();

        public Form1(string connString, int noParams, string paramTypes, string parentTable, string childTable, string selectParentCommand, string selectChildCommand, string deleteChildCommand, string updateChildCommand, string insertChildCommand)
        {
            this.connString = connString;
            this.noParams = noParams;
            this.paramTypes = paramTypes;
            this.parentTable = parentTable;
            this.childTable = childTable;
            this.selectParentCommand = selectParentCommand;
            this.selectChildCommand = selectChildCommand;
            this.deleteChildCommand = deleteChildCommand;
            this.updateChildCommand = updateChildCommand;
            this.insertChildCommand = insertChildCommand;
            InitializeComponent();

            int j = 0;

            for (int i = 0; i < noParams; i++)
            {
                Label label = new Label();
                label.Anchor = AnchorStyles.Left;
                label.Text = "Atr" + (i + 1).ToString() + ":";
                TextBox textBox = new TextBox();
                textBox.Anchor = AnchorStyles.Left | AnchorStyles.Right;
                textBox.Dock = DockStyle.Fill;

                string paramType = "";
                while (j < paramTypes.Length && paramTypes[j] != '_')
                {
                    paramType += paramTypes[j++];
                }
                j += 1;
                textBoxes.Add(i, new Tuple<TextBox, string>(textBox, paramType));
                flowLayoutPanel_Update.Controls.Add(label);
                flowLayoutPanel_Update.Controls.Add(textBox);
            }
            flowLayoutPanel_Update.Controls.Add(new Label());
            Button buttonUpdate = new Button();
            buttonUpdate.Click += buttonUpdate_Click;
            buttonUpdate.Text = "Update";
            buttonUpdate.Size = new Size(208, 29);
            flowLayoutPanel_Update.Controls.Add(buttonUpdate);
            Button buttonAdd = new Button();
            buttonAdd.Click += buttonAdd_Click;
            buttonAdd.Text = "Add";
            buttonAdd.Size = new Size(208, 29);
            flowLayoutPanel_Update.Controls.Add(buttonAdd);
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            try
            {
                using (SqlConnection conn = new SqlConnection(connString))
                {
                    conn.Open();
                    //MessageBox.Show(conn.State.ToString());
                    adapter.SelectCommand = new SqlCommand(selectParentCommand, conn);
                    adapter.Fill(ds, parentTable);
                    dataGridView_SpatiiDeAnimale.DataSource = ds.Tables[parentTable];
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }

        private void dataGridView_SpatiiDeAnimale_CellClick(object sender, DataGridViewCellEventArgs e)
        {
            DataGridViewRow selectedRow = dataGridView_SpatiiDeAnimale.CurrentRow;
            if (selectedRow == null)
                return;
            cod_parent = (int)selectedRow.Cells[0].Value;
            try
            {
                using (SqlConnection conn = new SqlConnection(connString))
                {
                    conn.Open();
                    //MessageBox.Show(conn.State.ToString());
                    adapter.SelectCommand = new SqlCommand(selectChildCommand, conn);
                    adapter.SelectCommand.Parameters.AddWithValue("@cod_parent", cod_parent);
                    if (ds.Tables.Contains(childTable))
                        ds.Tables[childTable].Clear();
                    adapter.Fill(ds, childTable);
                    dataGridView_Animale.DataSource = ds.Tables[childTable];
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }

        }

        private void dataGridView_Animale_CellClick(object sender, DataGridViewCellEventArgs e)
        {
            DataGridViewRow selectedRow = dataGridView_Animale.CurrentRow;
            if (selectedRow == null)
                return;
            cod_child = (int)selectedRow.Cells[0].Value;
        }

        private void buttonDelete_Click(object sender, EventArgs e)
        {
            try
            {
                using (SqlConnection conn = new SqlConnection(connString))
                {
                    conn.Open();
                    //MessageBox.Show(conn.State.ToString());
                    adapter.DeleteCommand = new SqlCommand(deleteChildCommand, conn);
                    adapter.DeleteCommand.Parameters.AddWithValue("@cod_child", cod_child);
                    adapter.DeleteCommand.ExecuteNonQuery();

                    adapter.SelectCommand = new SqlCommand(selectChildCommand, conn);
                    adapter.SelectCommand.Parameters.AddWithValue("@cod_parent", cod_parent);

                    if (ds.Tables.Contains(childTable))
                        ds.Tables[childTable].Clear();
                    adapter.Fill(ds, childTable);
                    //adapter.Update(ds, "Animale");

                    dataGridView_Animale.DataSource = ds.Tables[childTable];
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }

        private void buttonUpdate_Click(object sender, EventArgs e)
        {
            try
            {
                using (SqlConnection conn = new SqlConnection(connString))
                {
                    conn.Open();
                    //MessageBox.Show(conn.State.ToString());
                    adapter.UpdateCommand = new SqlCommand(updateChildCommand, conn);
                    for (int i = 0; i < noParams; i++)
                    {
                        TextBox textBox = textBoxes[i].Item1;
                        string type = textBoxes[i].Item2;
                        string arg = "param" + i.ToString();
                        if (type[0] == '!')
                        {
                            type = type.Substring(1);
                        }
                        if (type == "string")
                        {
                            string param = textBox.Text;
                            adapter.UpdateCommand.Parameters.AddWithValue(arg, param);
                        }
                        if (type == "int")
                        {
                            int param = int.Parse(textBox.Text);
                            adapter.UpdateCommand.Parameters.AddWithValue(arg, param);
                        }
                        if (type == "float")
                        {
                            float param = float.Parse(textBox.Text);
                            adapter.UpdateCommand.Parameters.AddWithValue(arg, param);
                        }
                        textBox.Text = "";
                    }
                    adapter.UpdateCommand.Parameters.AddWithValue("@cod_child", cod_child);
                    adapter.UpdateCommand.ExecuteNonQuery();

                    adapter.SelectCommand = new SqlCommand(selectChildCommand, conn);
                    adapter.SelectCommand.Parameters.AddWithValue("@cod_parent", cod_parent);

                    if (ds.Tables.Contains(childTable))
                        ds.Tables[childTable].Clear();
                    adapter.Fill(ds, childTable);

                    dataGridView_Animale.DataSource = ds.Tables[childTable];
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }

        private void buttonAdd_Click(object sender, EventArgs e)
        {
            try
            {
                using (SqlConnection conn = new SqlConnection(connString))
                {
                    conn.Open();
                    //MessageBox.Show(conn.State.ToString());
                    adapter.InsertCommand = new SqlCommand(insertChildCommand, conn);
                    for (int i = 0; i < noParams; i++)
                    {
                        TextBox textBox = textBoxes[i].Item1;
                        string type = textBoxes[i].Item2;
                        string arg = "param" + i.ToString();

                        if (type[0] == '!')
                        {
                            adapter.InsertCommand.Parameters.AddWithValue(arg, cod_parent);
                        }
                        else
                        {
                            if (type == "string")
                            {
                                string param = textBox.Text;
                                adapter.InsertCommand.Parameters.AddWithValue(arg, param);
                            }
                            if (type == "int")
                            {
                                int param = int.Parse(textBox.Text);
                                adapter.InsertCommand.Parameters.AddWithValue(arg, param);
                            }
                            if (type == "float")
                            {
                                float param = float.Parse(textBox.Text);
                                adapter.InsertCommand.Parameters.AddWithValue(arg, param);
                            }
                        }
                        textBox.Text = "";

                    }
                    adapter.InsertCommand.ExecuteNonQuery();

                    adapter.SelectCommand = new SqlCommand(selectChildCommand, conn);
                    adapter.SelectCommand.Parameters.AddWithValue("@cod_parent", cod_parent);

                    if (ds.Tables.Contains(childTable))
                        ds.Tables[childTable].Clear();
                    adapter.Fill(ds, childTable);

                    dataGridView_Animale.DataSource = ds.Tables[childTable];
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }
    }
}