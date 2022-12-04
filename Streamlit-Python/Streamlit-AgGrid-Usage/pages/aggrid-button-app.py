import streamlit as st 
import pandas as pd
from st_aggrid import AgGrid, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from database import *

# This demo is mainly from the suggestion on Community Post 
# https://www.youtube.com/channel/UCDMP6ATYKNXMvn2ok1gfM7Q/community?lb=UgkxMTe1HSFYPta6YDSZCXqkSCp2cKfyiYmU
# ".....Another suggestion for streamlit-aggrid features to explore is buttons inside the aggrid. 
# I think it would be interesting because there aren't many examples of that in the Streamlit forum.""
@st.experimental_memo
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')


st.header("AgGrid Demo `Part 3`")
with st.expander(' 🎉 What have we done untill now ? ', expanded=False):
    st.markdown('''
                
                ✅ 1. `Working` with AgGrid Table 
                
                ✅ 2. `Highlighting` AgGrid Table
                
                ✅ 3. `Deleting` rows in AgGrid Table
                ''')
with st.expander('🤩 What I plan to demonstrate today ? ', expanded=False):
    st.markdown('''
                
                ◻ 1. Implementing `button` within AgGrid table
                
                ◻ 2. Display any `update` made from the user-end
                
                ◻ 3. `Download` the AgGrid table
                
                ◻ 4. `Connect` to Database
                ''')

# Dump any DataFrame
d = {'Type':['Notebook', 'DVDs'] ,'Quantity': [1, 2],'Price': [400, 200]}
df = pd.DataFrame(data = d)

# Dump as AgGrid Table
# AgGrid(df)

# JavaScript function 
# api.applyTransaction({add: [{}]})   # This line would end row at the end always 
# Finding row index is important to add row just after the selected index
js_add_row = JsCode("""
function(e) {
    let api = e.api;
    let rowPos = e.rowIndex + 1; 
    api.applyTransaction({addIndex: rowPos, add: [{}]})    
};
"""     
)  

# cellRenderer with a button component.
# Resources:
# https://blog.ag-grid.com/cell-renderers-in-ag-grid-every-different-flavour/
# https://www.w3schools.com/css/css3_buttons.asp
cellRenderer_addButton = JsCode('''
    class BtnCellRenderer {
        init(params) {
            this.params = params;
            this.eGui = document.createElement('div');
            this.eGui.innerHTML = `
            <span>
                <style>
                .btn_add {
                    background-color: #71DC87;
                    border: 2px solid black;
                    color: #D05732;
                    text-align: center;
                    display: inline-block;
                    font-size: 12px;
                    font-weight: bold;
                    height: 2em;
                    width: 10em;
                    border-radius: 12px;
                    padding: 0px;
                }
                </style>
                <button id='click-button' 
                    class="btn_add" 
                    >&#x2193; Add</button>
            </span>
        `;
        }

        getGui() {
            return this.eGui;
        }

    };
    ''')

# Dump as AgGrid Table
# AgGrid(df)
gd = GridOptionsBuilder.from_dataframe(df)
gd.configure_default_column(editable=True)
gd.configure_column(field = '🔧',  
                    onCellClicked = js_add_row,
                    cellRenderer = cellRenderer_addButton,
                    lockPosition='left')
gridoptions = gd.build()
# This part for updating the Grid so that Streamlit doesnot rerun from whole
with st.form('Itenary') as f:
    st.header('Itenary List 🔖')
    response = AgGrid(df,
                    gridOptions = gridoptions, 
                    editable=True,
                    allow_unsafe_jscode = True,
                    theme = 'balham',
                    height = 200,
                    fit_columns_on_grid_load = True)
    st.write(" *Note: Don't forget to hit enter ↩ on new entry.*")
    st.form_submit_button("Confirm item(s) 🔒", type="primary")
# Dump                     )
res = response['data']
st.table(res) 

col1,col2 = st.columns(2)
# https://docs.streamlit.io/knowledge-base/using-streamlit/how-download-pandas-dataframe-csv
csv = convert_df(response['data'])
col1.download_button(
   "Press to Download 🗳️",
   csv,
   "file.csv",
   "text/csv",
   key='download-csv'
)

if col2.button("Update to Database 🚀 "):
    send_to_database(res)
    