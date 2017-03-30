import tkinter
import glob
import os
import argparse

def parse_argument():
    parser = argparse.ArgumentParser(
        prog='marker',
        description="markes articles",
    )


    parser.add_argument(
        'articlesNum',
        help='number of articles to mark',
        nargs=1,
    )

    return parser.parse_args()


def like() :
    with open("interesting.txt", 'a') as interesting:
        interesting.write(file +'\n')
    try:
        page = filegen.__next__()
        text_window.delete('1.0', tkinter.END)
        text_window.insert(1.0, page)
        root.update()
    except StopIteration:
        root.destroy()

def dislike() :
    with open("boring.txt", 'a') as boring:
        boring.write(file +'\n')
    try:
        page = filegen.__next__()
        text_window.delete('1.0', tkinter.END)
        text_window.insert(1.0, page)
        root.update()
    except StopIteration:
        root.destroy()


def file_generator(articles_num):
    global file
    for file in glob.glob("../crawler/articles/text/" + '?*.txt'):
        if articles_num == 0:
            raise StopIteration
        with open(file, 'r') as article:
            page = article.read()
            articles_num -= 1;
            yield page


def main():
    open('interesting.txt', 'w').close()
    open('boring.txt', 'w').close()

    global filegen, text_window, root
    args = parse_argument()
    articles_num = int(args.articlesNum[0]);
    filegen = file_generator(articles_num)
    root = tkinter.Tk()
    root.geometry('600x600')
    page = filegen.__next__()

    butLike = tkinter.Button(root,text='like',width=10,height=2,bg='black',fg='red',font='arial 14', command=like)
    butDislike = tkinter.Button(root,text='dislike',width=10,height=5,
                                bg='black',fg='red',font='arial 14', command=dislike)

    text_window = tkinter.Text(root, width=80, height=30, font="Verdana 12")
    text_window.insert(1.0, page)

    text_window.pack()
    butLike.pack()
    butDislike.pack()
    root.title('Article marker')
    root.mainloop()





if __name__ == '__main__':
    main()