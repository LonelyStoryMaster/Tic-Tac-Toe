import Util

class GameSquare():
    def __init__(self, origin, square_size):
        self.origin = origin
        self.square_size = square_size
        self.end_point = self.__calc_end_point()
        self.center_point = self.__calc_centerpoint()
        self.winner = Util.Winners.NONE

    # Calculating the outside bounds of the square
    def __calc_end_point(self):
        width = self.origin[0] + self.square_size
        height = self.origin[1] + self.square_size
        return ( width, height )

    def __calc_centerpoint(self):
        centerX = self.origin[0] + int( self.square_size / 2 )
        centerY = self.origin[1] + int( self.square_size / 2 )
        return ( centerX, centerY )

    # Checking if the desired position is within the bounds of the square
    def is_In_Square(self, pos_to_check):
        withinXBounds = Util.within_tol( pos_to_check[0], self.origin[0], self.end_point[0] )
        withinYBounds = Util.within_tol( pos_to_check[1], self.origin[1], self.end_point[1] )
        return ( withinXBounds and withinYBounds )

    def get_Winner(self):
        return self.winner

    def set_Winner(self, winner):
        self.winner = winner

    def get_End_Point(self):
        return self.end_point

    def get_Center_Point(self):
        return self.center_point

    def get_Square_Size(self):
        return self.square_size

    def get_Origin(self):
        return self.origin