import Util

class GameSquare():
    def __init__(self, origin, side_length):
        self.origin = origin
        self.side_length = side_length
        self.end_point = self.__calc_end_point()
        self.center_point = self.__calc_centerpoint()
        self.winner = Util.Winners.NONE

    # Calculating the outside bounds of the square
    def __calc_end_point(self):
        width = self.origin[0] + self.side_length
        height = self.origin[1] + self.side_length
        return ( width, height )

    def __calc_centerpoint(self):
        centerX = self.origin[0] + int( self.side_length / 2 )
        centerY = self.origin[1] + int( self.side_length / 2 )
        return ( centerX, centerY )

    # Checking if the desired position is within the bounds of the square
    def is_In_Square(self, pos_to_check):
        withinXBounds = Util.within_Range( pos_to_check[0], self.origin[0], self.end_point[0] )
        withinYBounds = Util.within_Range( pos_to_check[1], self.origin[1], self.end_point[1] )
        return ( withinXBounds and withinYBounds )

    def get_Winner(self):
        return self.winner

    def set_Winner(self, winner):
        self.winner = winner

    def get_End_Point(self):
        return self.end_point

    def get_Center_Point(self):
        return self.center_point

    def get_Side_Length(self):
        return self.side_length

    def get_Origin(self):
        return self.origin