from threading import Thread
import tkinter as tk
import math
import time


class C(tk.Frame):
    def __init__(self, master, tamanho, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.tamanho = tamanho
        self.intervalo = 0.01
        self.velocidade = math.pi/100
        self.terminado = False

        self._canvas = tk.Canvas(
            self,
            height=tamanho,
            width=tamanho
        )
        self._canvas.pack()

        self._c = self._canvas.create_polygon(
            self._pontos(), fill='green',
            outline='black'
        )
        
        self._taxa = 0.0
        self._eixo_de_rotacao = self.tamanho / 2
    
    def destroy(self):
        self.terminado = True
        super().destroy()

    def _pontos(self):
        return (
            (-.25 * self.tamanho, 0.50 * self.tamanho),  # a
            (0.00 * self.tamanho, 0.25 * self.tamanho),  # b
            (0.25 * self.tamanho, 0.50 * self.tamanho),  # c
            (0.75 * self.tamanho, 0.00 * self.tamanho),  # d
            (1.00 * self.tamanho, 0.25 * self.tamanho),  # e
            (0.25 * self.tamanho, 1.00 * self.tamanho),  # f
        )

    def _rotacao_horizontal(self, p, t):
        x = (p[0] - self._eixo_de_rotacao) * t
        return x + self._eixo_de_rotacao, p[1]

    def _animacao(self):
        while not self.terminado:
            self._taxa = math.fmod(
                self._taxa + self.velocidade, 2*math.pi)
            pontos = [
                i
                for point in self._pontos()
                for i in self._rotacao_horizontal(
                    point, math.sin(self._taxa)
                )
            ]
            self._canvas.coords(self._c, pontos)
            time.sleep(self.intervalo)

    def animar(self):
        Thread(target=self._animacao).start()


if __name__ == '__main__':
    root = tk.Tk()
    app = C(root, 400)
    app.pack()
    app.animar()
    root.mainloop()
