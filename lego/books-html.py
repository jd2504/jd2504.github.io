import os
import pandas as pd


print('Writing books.txt to HTML... ', end='')

path = './lego/'
github_path = 'https://jd2504.github.io/lego/'
t_read_path = path + 'read.txt'
t_queue_path = path + 'read_queue.txt'
h_head_path = path + 'head.html'
h_tail_path = path + 'tail.html'
h_read_path = path + 'read.html'
h_queue_path = path + 'read_queue.html'


read_in = pd.read_csv(t_read_path, sep='|').sort_values(by=['read'], ascending=False)

# create hyperlink if file exists
def create_link(readid):
    html_path = os.path.join(path, f"{readid}.html")
    txt_path = os.path.join(path, f"{readid}.txt")
    pdf_path = os.path.join(path, f"{readid}.pdf")

    github_html_path = f"{github_path}{readid}.html"
    github_txt_path = f"{github_path}{readid}.txt"
    github_pdf_path = f"{github_path}{readid}.pdf"

    # check in priority order: html > txt > pdf
    if os.path.exists(html_path):
        return f'<a href="{github_html_path}">{readid}</a>'
    elif os.path.exists(txt_path):
        return f'<a href="{github_txt_path}">{readid}</a>'
    elif os.path.exists(pdf_path):
        return f'<a href="{github_pdf_path}">{readid}</a>'
    else:
        return readid
    
read_in['readid'] = read_in['readid'].apply(create_link)

read_html = read_in.to_html(
    table_id='readTxt',
    index=False,
    justify='left',
    columns=[
        'readid', 'title', 'author', 'published', 'read', 'keywords'
    ],
    escape=False
)

read_html = read_html.replace('<th>title</th>', '<th onclick="sortTable(0)">title</th>')
read_html = read_html.replace('<th>author</th>', '<th onclick="sortTable(1)">author</th>')
read_html = read_html.replace('<th>published</th>', '<th onclick="sortTable(2)">published</th>')
read_html = read_html.replace('<th>read</th>', '<th onclick="sortTable(3)">read</th>')


with open(h_head_path, 'r') as f:
    head = f.read()
with open(h_tail_path, 'r') as f:
    tail = f.read()
with open(h_read_path, 'w') as f:
    f.write(head)
    f.write(read_html)
    f.write(tail)


queue = pd.read_csv(t_queue_path, sep='|')
queue_html = queue.to_html()
with open(h_queue_path, 'w') as f:
    f.write(queue_html)

    

def txt_to_html(df, output_file, format_col=False):
    df_in = pd.read_csv(df, sep='|')
    # df_in = df_in[['readid', 'format', 'title', 'author', 'published', 'read', 'keywords']]
    # print(df_in.columns.tolist())
    if not format_col:
        df_in = df_in.drop(columns=['format'])

    df_html = df_in.to_html(index=False)

    with open(output_file, 'w') as f:
        f.write(df_html)

#txt_to_html('~/blurble/read.txt', 'read.html', format_col=False)
#txt_to_html('~/blurble/read_queue.txt', 'read_queue.html', format_col=False)


print('\nDone')
