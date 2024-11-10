from flask import Flask, render_template, jsonify
import polars as pl
from app.process import ProcessMonthData, ProcessYearData

app = Flask(__name__)

@app.route("/")
def home():
    df_month = pl.read_csv("app/data/fpidata_monthwise.csv")
    month_data = ProcessMonthData(df_month)
    x_total,y_total = month_data.monthlytotal()
    x_equity,y_equity = month_data.monthlyequity()
    x_funds,y_funds = month_data.monthlyfunds()
    cy_total = month_data.yeartotal()
    cy_debt = month_data.debttotal()
    cy_hybrid = month_data.hybridtotal()


    df_year = pl.read_csv("app/data/fpidata_financialyearwise.csv")
    year_data = ProcessYearData(df_year)
    x_yearly,y_yearly = year_data.yearlytotal()
    x_cum,y_cum = year_data.yearlycumtotal()



    return render_template("home.html",x_total=x_total,y_total=y_total, \
                            x_equity=x_equity,y_equity=y_equity, \
                            x_funds=x_funds,y_funds=y_funds, \
                            x_yearly=x_yearly,y_yearly=y_yearly, \
                            x_cum=x_cum,y_cum=y_cum, \
                            cy_total=cy_total, cy_debt=cy_debt, \
                            cy_hybrid=cy_hybrid)