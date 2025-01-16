import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from bokeh.models import ColumnDataSource, Range1d, RangeTool, Div, CustomJS, Legend
from bokeh.plotting import figure, output_file, save
from bokeh.layouts import column

def generate_test_data():
    # 產生30天範圍的日期，每天一筆數據
    start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=29)
    end_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    date_rng = pd.date_range(start=start_date, end=end_date, freq='D')
    values = np.random.uniform(80, 120, len(date_rng))  # 隨機生成值在 100 上下震盪 20%
    df = pd.DataFrame({'date': date_rng, 'value': values})
    df.to_csv('test_data.csv', index=False)

def show_data(df, data_path, label):
    # 初始化數據
    df['date'] = pd.to_datetime(df['date'])  # 確保日期為 datetime 格式
    df = df[-30:]
    dates = np.array(df['date'], dtype=np.datetime64)
    values = df['value']
    
    # 計算 n 天移動平均
    avg_day = 7
    rolling_avg = pd.Series(values).rolling(window=avg_day).mean()

    # 將資料放入 ColumnDataSource
    source = ColumnDataSource(data=dict(date=dates, values=values, rolling_avg=rolling_avg))

    # 初始範圍
    initial_start_avg_day = dates[-avg_day]  # 最後 n 天為初始範圍
    initial_start3 = dates[-3]  # 最後 3 天為初始範圍
    initial_end = dates[-1]     # 到最新日期

    # 計算初始平均值
    initial_mask = (dates >= np.datetime64(initial_start3)) & (dates <= np.datetime64(initial_end))
    initial_values = values[initial_mask]
    initial_avg = np.mean(initial_values) if len(initial_values) > 0 else "N/A"

    # 標題
    title = f"<b>{label}{len(initial_values)}天平均: {initial_avg:.2f} 單位</b>" if initial_avg != "N/A" else f"<b>{label}平均值: N/A</b>"
    average_div = Div(text=title, width=800, height=30)

    # 範圍選擇器
    select = figure(height=130, width=800, x_axis_type="datetime", x_range=(initial_start_avg_day - np.timedelta64(12, 'h'), initial_end + np.timedelta64(12, 'h')), y_range=(0, 150),
                    tools="xpan", toolbar_location=None, background_fill_color="#efefef", )

    # 添加每日數值柱狀圖
    select.vbar(x='date', top='values', width=3e7, source=source, color="blue", legend_label="每日數值")

    # 添加 n 天移動平均紅線
    select.line(x='date', y='rolling_avg', source=source, line_width=3, color="red", legend_label=f"{avg_day}天平均值")
    # select.legend.visible = False

    # 範圍選擇器
    range_tool = RangeTool(x_range=Range1d(initial_start3, initial_end))
    range_tool.overlay.fill_color = "navy"
    range_tool.overlay.fill_alpha = 0.2
    select.add_tools(range_tool)

    # JavaScript 回調函數
    callback = CustomJS(args=dict(source=source, avg_div=average_div, x_range=range_tool.x_range,label=label), code="""
        const data = source.data;
        const dates = data['date'];
        const values = data['values'];
        const start = x_range.start;
        const end = x_range.end;

        let sum = 0;
        let count = 0;

        for (let i = 0; i < dates.length; i++) {
            if (dates[i] >= start && dates[i] <= end) {
                sum += values[i];
                count += 1;
            }
        }

        if (count > 0) {
            const avg = sum / count;
            avg_div.text = `<b>${label}${count}天平均: ${avg.toFixed(2)} 單位</b>`;
        } else {
            avg_div.text = "<b>平均值: N/A</b>";
        }
    """)

    # 綁定回調函數到 x_range
    range_tool.x_range.js_on_change('start', callback)
    range_tool.x_range.js_on_change('end', callback)

    output_file(data_path)
    save(column(average_div, select))


if __name__ == '__main__':
    generate_test_data()
    df = pd.read_csv('test_data.csv')
    show_data(df,"static_average_bar_chart.html", label='營養成分')
