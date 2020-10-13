from Renderer import Renderer
from Model import Model
from math import radians
import numpy as np
import MatrixShop

class Intermediary:
    
    def __init__(self, model: Model, project_matrix, model_matrix, color):
        self.model = model
        self.project_matrix = project_matrix
        self.model_matrix = model_matrix
        self.color = color
        self.model.color = color
    
    def getAllFacesVerts(self):
        return self.model.getAllFacesVerts()

    def render_one(self, context):
        Renderer.render_one(self.model, self.project_matrix, self.model_matrix, context)

    @staticmethod
    def render_all_colors(intermediarys, context):
        models = [instan.model for instan in intermediarys]
        some_i = intermediarys[0]
        Renderer.render_all_color(models, some_i.project_matrix, some_i.model_matrix, context)
    
    @staticmethod
    def render_all_z_mask(intermediarys, context):
        models = [instan.model for instan in intermediarys]
        some_i = intermediarys[0]
        Renderer.render_all_z_mask(models, some_i.project_matrix, some_i.model_matrix, context)
    
    @staticmethod
    def prerender_all(intermediarys, context):
        models = [instan.model for instan in intermediarys]
        some_i = intermediarys[0]
        return Renderer.prerender_all(models, some_i.project_matrix, some_i.model_matrix, context)
    
    @staticmethod
    def draw_color_mask(color_mask, context):
        Renderer.render_from_color_mask(color_mask, context)
    
    @staticmethod
    def draw_z_mask(z_mask, context):
        Renderer.render_from_z_mask(z_mask, context)

    @staticmethod
    def scale_x_more(fig):
        fig.model_matrix = fig.model_matrix @ MatrixShop.dilation(1.01, 1, 1)

    @staticmethod
    def scaleXLess(fig):
        fig.model_matrix = fig.model_matrix @ MatrixShop.dilation(0.99, 1, 1)
    
    @staticmethod
    def scaleYMore(fig):
        fig.model_matrix = fig.model_matrix @ MatrixShop.dilation(1, 1.01, 1)
    
    @staticmethod
    def scaleYLess(fig):
        fig.model_matrix = fig.model_matrix @ MatrixShop.dilation(1, 0.99, 1)
    
    @staticmethod
    def scaleZMore(fig):
        fig.model_matrix = fig.model_matrix @ MatrixShop.dilation(1, 1, 1.1)
    
    @staticmethod
    def scaleZLess(fig):
        fig.model_matrix = fig.model_matrix @ MatrixShop.dilation(1, 1, 0.99)
    
    @staticmethod
    def reflectionX(fig):
        fig.model_matrix = fig.model_matrix @ MatrixShop.reflectionX()
    
    @staticmethod
    def reflectionY(fig):
        fig.model_matrix = fig.model_matrix @ MatrixShop.reflectionY()
    
    @staticmethod
    def reflectionZ(fig):
        fig.model_matrix = fig.model_matrix @ MatrixShop.reflectionZ()
    
    @staticmethod
    def translationXRight(fig):
        fig.model_matrix = fig.model_matrix @ MatrixShop.translation(0.1, 0, 0)
    
    @staticmethod
    def translationYRight(fig):
        fig.model_matrix = fig.model_matrix @ MatrixShop.translation(0, 0.1, 0)
    
    @staticmethod
    def translationZRight(fig):
        fig.model_matrix = fig.model_matrix @ MatrixShop.translation(0, 0, 0.1)
    
    @staticmethod
    def translationXLeft(fig):
        fig.model_matrix = fig.model_matrix @ MatrixShop.translation(-0.1, 0, 0)
    
    @staticmethod
    def translationYLeft(fig):
        fig.model_matrix = fig.model_matrix @ MatrixShop.translation(0, -0.1, 0)
    
    @staticmethod
    def translationZLeft(fig):
        fig.model_matrix = fig.model_matrix @ MatrixShop.translation(0, 0, -0.1)
    
    @staticmethod
    def rotationXRight(fig):
        fig.model_matrix = fig.model_matrix @ MatrixShop.rotationX(radians(3))
    
    @staticmethod
    def rotationYRight(fig):
        fig.model_matrix = fig.model_matrix @ MatrixShop.rotationY(radians(3))
    
    @staticmethod
    def rotationZRight(fig):
        fig.model_matrix = fig.model_matrix @ MatrixShop.rotationZ(radians(3))
    
    @staticmethod
    def rotationXLeft(fig):
        fig.model_matrix = fig.model_matrix @ MatrixShop.rotationX(-radians(6))
    
    @staticmethod
    def rotationYLeft(fig):
        fig.model_matrix = fig.model_matrix @ MatrixShop.rotationY(-radians(6))
    
    @staticmethod
    def rotationZLeft(fig):
        fig.model_matrix = fig.model_matrix @ MatrixShop.rotationZ(-radians(6))
    
    @staticmethod
    def orthoPoject(fig):
        fig.project_matrix = MatrixShop.orthoPoject()
    
    @staticmethod
    def perspectiveProj(fig):
        fig.project_matrix = MatrixShop.perspectiveProject(3)
        
    @staticmethod
    def kabinetProj(fig):
        fig.project_matrix = MatrixShop.kabinetProject()
    
    @staticmethod
    def cavalieProj(fig):
        fig.project_matrix = MatrixShop.cavalerProject()

    def scale(self, matrix, x, y, z):
        self.model_matrix = matrix @ MatrixShop.dilation(x, y, z)

    def figuresToAnimationFrame(self, kx, ky, kz):
        def _generator(k) :
            start = 1
            n = (k - start) * 0.7
            yield from np.linspace(start, start + n, 100)

            start += n
            n = (k - start) / 2
            yield from np.linspace(start, start + n, 130)

            start += n
            yield from np.linspace(start, k + n, 160)

        start_matrix = np.copy(self.model_matrix)
        generator = zip(_generator(kx), _generator(ky), _generator(kz))

        return (self.scale(start_matrix, x, y, z) for x, y, z in generator)