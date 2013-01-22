#!/usr/bin/python
#encoding=utf-8
'''
Conway 's game of life , python version using Tkinter

details of this game:
http://en.wikipedia.org/wiki/Conway%27s_Game_of_Life

author : dawn110110@gmail.com
start date : 2012-Jan-18

'''
from Tkinter import *

class TkPeriodicCallMixin(object):
    ''' periodic call '''
    interval = 300 # 1 second
    running = False
    def _loop(self):
        self.polling_callback()
        if self.running:
            self.after(self.interval,self._loop)
    def polling_callback(self,*args,**kargs):
        ''' to be rewrite '''
        print self,id(self)
    def start_polling(self):
        self.running = True
        self._loop()
    def stop_polling(self):
        self.running = False

class Grid(Canvas,TkPeriodicCallMixin):
    ''' the drawing widgets '''
    COLOR_MAP = {
        0:'#FFDDDD',
        8:'#FF0000', # red stands for crowd
        7:'#EE3333',
        6:'#DD4444',
        5:'#BB5555',
        4:'#996666',
        3:'#CCCC00', 
        2:'#FFEE00', # yellow stands for stable 
        1:'#339999'
    }
    def __init__(self,*args,**kargs):
        kargs['width'] = 600
        kargs['height'] = 400
        kargs['bg'] = 'grey'
        Canvas.__init__(self,*args,**kargs)
        # self.create_rectangle(0,0,600,400,fill='red')
        # self.create_rectangle(10,10,590,390,fill='white')

        self._size = (60,40)
        self.conway_map = Conway_Map(60,40)# create grid
        self.draw()
        self.start_polling()

    def polling_callback(self):
        print 'in polling'
        self.conway_map.update()
        self.draw()

    def draw(self):
        self.delete(ALL)
        self.create_rectangle(0,0,600,400,fill='grey')
        self.create_rectangle(10,10,590,390,fill='white')
        for x in xrange(60):
            self.create_line(10+10*x,10, 10+10*x, 390, fill="grey",dash=(4, 4))
        for y in xrange(40):
            self.create_line(10, 10+10*y,590, 10+10*y, fill="grey",dash=(4, 4))
        for i in xrange(60):
            for j in xrange(40):
                if self.conway_map.map[i][j]:
                    color = self.COLOR_MAP[self.conway_map.around_count[i][j]]
                    self.create_rectangle(10*i+10,10*j+10,10*i+20,10*j+20,fill=color)
    def god_click(self,x,y):
        ''' 
        callback
        click by the god, x y are clicks by the user,
        '''
        if x<590 and x>10 and y>10 and y<390:
            i,j =(x-15)/10,(y-15)/10
            self.create_rectangle(10*i+10,10*j+10,10*i+20,10*j+20,fill='black') # draw right now
            self.conway_map.god_click(i,j)
    def right_click(self,x,y):
        ''' 
        callback
        (right click) click by the god, x y are clicks by the user,
        '''
        if x<590 and x>10 and y>10 and y<390:
            i,j =(x-15)/10,(y-15)/10
            self.create_rectangle(10*i+10,10*j+10,10*i+20,10*j+20,fill='white') # draw right now
            self.conway_map.map[i][j]=0 # set empty



class GridWindow(object):
    ''' main window '''
    def __init__(self):
        self.root = Tk()
        self.root.minsize(650,450)
        self.root.title("conway's game of life, python version")

        descrition = u"conway 's game of life\npowered by Dawn http://orzdawn.com\n\nleft click on the grid to make new lives\nright click to kill lives"
        self.lb2 = Label(text=descrition)
        self.lb2.pack()

        self.grid = Grid(self.root)
        self.grid.pack()
        self.grid.bind("<Button-1>",self.left_click)
        self.grid.bind("<B1-Motion>",self.left_click)
        self.grid.bind("<Button-2>",self.right_click)
        self.grid.bind("<B2-Motion>",self.right_click)

        self.paused = False
        self.go_pause_btn = Button(self.root,text=u"|| pause",command=self.go_pause)
        self.go_pause_btn.pack()

        self.one_step_btn = Button(self.root,text=u'go one step',command=self.one_step)
        self.one_step_btn.pack()

        self.clear_all_btn = Button(self.root,text=u'clear all',command=self.clear_all)
        self.clear_all_btn.pack()

        self.lb1 = Label(text="update interval(ms):")
        self.lb1.pack()
        self.speed_scale = Scale(self.root,from_=10,to=1000,orient = HORIZONTAL, command= self.speed_change)
        self.speed_scale.set(300)
        self.speed_scale.pack()
    def speed_change(self,val):
        #val = self.speed_scale.get()
        print 'speed_scale=%r'%val
        self.grid.interval = int(val)
    def go_pause(self):
        if self.paused:
            self.grid.start_polling()
            self.paused = False
            self.go_pause_btn['text']=u'|| pause'
        else:
            self.grid.stop_polling()
            self.paused = True
            self.go_pause_btn['text']=u'> go'
    def one_step(self):
        self.grid.polling_callback()
    def clear_all(self):
        self.grid.conway_map.clear_all()
        self.grid.draw()

    def run(self):
        self.root.mainloop()

    def left_click(self,event):
        print "left,mouse pos: %r,%r"%(event.x,event.y),
        self.grid.god_click(event.x,event.y)
    def right_click(self,event):
        print "right,mouse pos: %r,%r"%(event.x,event.y),
        self.grid.right_click(event.x,event.y)

class Conway_Map(object):
    ''' data model '''
    def __init__(self,x,y):
        self.size = (x,y) # 40(y height) 60(y width)
        self.map = [[0 for i in range(y)] for j in range(x)]
        self.around_count = [[0 for i in range(y)] for j in range(x)] # counting arounds
        print len(self.map),' ',len(self.map[0])
    def update(self):
        ''' update the self.map '''
        self.count_map()
        for i in xrange(60):
            for j in xrange(40):
                if self.around_count[i][j] == 2:
                    pass
                elif self.around_count[i][j] == 3:
                    self.map[i][j] = 1
                else:
                    self.map[i][j] = 0
        self.count_map()
    def count_map(self):
        ''' 
        count the map. store result in self.around_count
        around every block, count the alive blocks around it.
        '''
        for i in xrange(60):
            for j in xrange(40):
                arounds = [
                            (i,(j+1)%40),
                            (i,(j-1)%40),
                            ((i-1)%60,j),
                            ((i+1)%60,j),
                            ((i+1)%60,(j+1)%40),
                            ((i+1)%60,(j-1)%40),
                            ((i-1)%60,(j+1)%40),
                            ((i-1)%60,(j-1)%40),]

                self.around_count[i][j] = 0
                for i_r,j_r in arounds:
                    self.around_count[i][j] += self.map[i_r][j_r] 
    def god_click(self,x,y):
        '''
        callback
        '''
        print "grid_pos = (%d,%d)"%(x,y)
        self.map[x][y] = 1 # set life
    def clear_all(self):
        for i in xrange(60):
            for j in xrange(40):
                self.map[i][j] = 0
if __name__=="__main__":
    win = GridWindow()
    win.run()