# Python module for processing data
import polars as pl

class ProcessMonthData:
    """
    class for csv data processing
    """
    def __init__(self, df):
        self.df = df
    
    
    def __repr__(self):
        return self.df


    def process(self):
        "Function for adding columns and checking data"
        processed_df = self.df.clone()
        columns = processed_df.columns
        columns = [col.lower() for col in columns]
        processed_df.columns = columns

        processed_df = processed_df.with_columns(
            mf_total = pl.col("mf_equity") + pl.col("mf_debt") + \
                       pl.col("mf_hybrid") + pl.col("mf_solution oriented") + \
                       pl.col("mf_other"),
            debt_total = pl.col("debt-general limit") + pl.col("debt-vrr") + \
                         pl.col("debt-far"),
            cumulative = pl.col("total").cum_sum()
            )

        return processed_df
    
    def monthlytotal(self):
        """
        Function for returning total values for mothly chart
        """
        total_df = self.process()
        x = total_df['month'][:-1].to_list()
        y = total_df['total'][:-1].to_list()
        return (x,y)

    def monthlyfunds(self):
        """
        Function for returning mutual fund values for mothly chart
        """
        funds_df = self.process()
        x = funds_df['month'].to_list()
        y = funds_df['mf_total'].to_list()
        return (x,y)

    def monthlyequity(self):
        """
        Function for returning equity values for mothly chart
        """
        equity_df = self.process()
        x = equity_df['month'].to_list()
        y = equity_df['equity'].to_list()
        return (x,y)

    def yeartotal(self):
        """
        Function for returning calender year total
        """
        cy_total = self.process()
        x = cy_total['cumulative'][:-1].to_list()
        return x

    def debttotal(self):
        """
        Function for returning calender year debt total
        """
        cy_debt = self.process()
        x = cy_debt['debt_total'].to_list()
        return x

    def hybridtotal(self):
            """
            Function for returning calender year debt total
            """
            cy_hybrid = self.process()
            x = cy_hybrid['hybrid'].to_list()
            return x
    

class ProcessYearData:
    """
    class for processing yearly data
    """
    def __init__(self,df):
        self.df = df

    
    def yearlytotal(self):
        """
        function for returning total values for yearly chart
        """
        x = self.df['fy'][:-1].to_list()
        y = self.df['total'][:-1].to_list()
        return (x,y)

    def yearlycumtotal(self):
        """
        function for returning cumulative total values for yearly chart
        """
        x = self.df['fy'][:-1].to_list()
        y = self.df['cumulative'][:-1].to_list()
        return (x,y)

    def yearlyequity(self):
        """
        function for returning equity values for yearly chart
        """
        pass



if __name__ == '__main__':
    df = pl.read_csv("./data/fpidata_monthwise.csv")
    data = ProcessMonthData(df)
    print(data.process().columns)
    #x,y = data.monthlyfunds()
    #print(x)
    #print(y)

    df_year = pl.read_csv("./data/fpidata_financialyearwise.csv")
    year_data = ProcessYearData(df_year)
    x_yearly,y_yearly = year_data.yearlytotal()
    print(x_yearly)
    print(y_yearly)


