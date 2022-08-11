from threading import Thread

import tkinter as tk
import math
import time


class Q(tk.Frame):
    def __init__(self, master, tamanho, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.tamanho = tamanho
        self.velocidade = math.pi / 100
        self.intervalo = 0.01
        self.terminado = False

        self._taxa = .0
        self._eixo_de_rotacao = (tamanho / 2,) * 2

        self._canvas = tk.Canvas(
            self, height=tamanho,
            width=tamanho
        )
        self._canvas.pack()

        self._desenho = self._canvas.create_polygon(
            self._pontos, fill='gold', outline='black'
        )

    @property
    def _pontos(self):
        return (
            (.25 * self.tamanho, .25 * self.tamanho),  # a
            (.75 * self.tamanho, .25 * self.tamanho),  # b
            (.75 * self.tamanho, .75 * self.tamanho),  # c
            (.25 * self.tamanho, .75 * self.tamanho),  # d
        )

    def _girador(self, p0, eixo, t):
        x = p0[0] - eixo[0]
        y = p0[1] - eixo[1]
        vector = \
            x * math.cos(t) - y * math.sin(t), \
            x * math.sin(t) + y * math.cos(t)

        return vector[0] + eixo[0], vector[1] + eixo[1]

    def _animacao(self):
        while not self.terminado:
            self._taxa = math.fmod(
                self._taxa + self.velocidade, 2*math.pi)
            pontos = [
                i
                for point in self._pontos
                for i in self._girador(
                    point, self._eixo_de_rotacao,
                    self._taxa
                )
            ]
            self._canvas.coords(self._desenho, pontos)
            time.sleep(self.intervalo)
    
    def destroy(self):
        self.terminado = True
        super().destroy()

    def animar(self):
        Thread(target=self._animacao).start()


if __name__ == '__main__':
    root = tk.Tk()
    app = Q(root, 400)
    app.pack()
    app.animar()
    root.mainloop()
