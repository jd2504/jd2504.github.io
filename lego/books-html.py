import os
import pandas as pd


print('Writing books.txt to HTML... ', end='')

path = './lego/'
t_read_path = path + 'read.txt'
t_queue_path = path + 'read_queue.txt'
h_head_path = path + 'head.html'
h_tail_path = path + 'tail.html'
h_read_path = path + 'read.html'
h_queue_path = path + 'read_queue.html'


read_in = pd.read_csv(t_read_path, sep='|').sort_values(by=['read'], ascending=False)

read_html = read_in.to_html(
    table_id='readTxt',
    index=False,
    justify='left',
    columns=[
        'readid', 'title', 'author', 'published', 'read', 'keywords'
    ]
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

# read = pd.read_csv('./read.txt', sep='|')
# read_out = read[['Title', 'Publication date', 'Author', 'Read']]
# read_html = read_out.to_html(index=False)

# queue = pd.read_csv('./books_queue.txt', sep='|')
# queue_html = queue.to_html(index=False)

# with open('read.html', 'w') as f:
    # f.write(read_html)
# with open('books_queue.html', 'w') as f:
    # f.write(queue_html)


print('Done')
