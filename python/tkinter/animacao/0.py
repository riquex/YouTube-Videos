from threading import Thread
from tkinter import Canvas
from tkinter import Frame
from tkinter import Tk
from time import sleep
from math import fmod
from math import sin
from math import pi


class X(tk.Frame):
    def __init__(self, master, tamanho: int, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.tamanho = tamanho
        self.intervalo = 0.01
        self.terminado = False
        self.velocidade = pi/100

        self._canvas = tk.Canvas(master, height=tamanho, width=tamanho)
        self._canvas.pack()
        self._x = self._canvas.create_polygon(self._pontos(), fill='red', outline='black')
        self._taxa: float = .0
        self._centro: tuple[float, float] = (tamanho/2, tamanho/2)

    def _pontos(self):
        return (
            (0.0 * self.tamanho, .25 * self.tamanho),  # a
            (.25 * self.tamanho, 0.0 * self.tamanho),  # b
            (.50 * self.tamanho, .25 * self.tamanho),  # c
            (.75 * self.tamanho, 0.0 * self.tamanho),  # d
            (1.0 * self.tamanho, .25 * self.tamanho),  # e
            (.75 * self.tamanho, .50 * self.tamanho),  # f
            (1.0 * self.tamanho, .75 * self.tamanho),  # g
            (.75 * self.tamanho, 1.0 * self.tamanho),  # h
            (.50 * self.tamanho, .75 * self.tamanho),  # i
            (.25 * self.tamanho, 1.0 * self.tamanho),  # j
            (0.0 * self.tamanho, .75 * self.tamanho),  # k
            (.25 * self.tamanho, .50 * self.tamanho),  # l
        )

    def _taxa_circular(self, x: float) -> float:
        '''
        Graph -> https://www.desmos.com/calculator/293vv4my1m
        '''
        return (sin((2*x)-(pi/2))+1)/2

    def destroy(self):
        self.terminado = True
        super().destroy()

    def _aproximar_pontos(
            self,
            p0: tuple[float, float],
            p1: tuple[float, float],
            t: float) -> tuple[float, float]:
        x = p1[0] - p0[0]
        y = p1[1] - p0[1]
        vetor = x * t, y * t
        return p0[0] + vetor[0], p0[1] + vetor[1]

    def _animacao(self):
        while not self.terminado:
            self._taxa = fmod(self._taxa + self.velocidade, 2 * pi)
            pontos = [
                p
                for ponto in self._pontos()
                for p in self._aproximar_pontos(
                    ponto, self._centro, self._taxa_circular(self._taxa)
                )
            ]
            self._canvas.coords(self._x, pontos)
            sleep(self.intervalo)

    def animar(self):
        Thread(target=self._animacao).start()


if __name__ == '__main__':
    root = tk.Tk()
    app = X(root, 400)
    app.pack()
    app.animar()
    root.mainloop()
