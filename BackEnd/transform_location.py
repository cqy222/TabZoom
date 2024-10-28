import uuid
import os, random
import json


# 这个函数在原始提取的block的insight信息中，增加了block之间关系的信息 
def generate_block_link_new(insight_vis_list):
    # Iterate over each dictionary in the list
    for current in insight_vis_list:
        # Initialize all required relationships as empty lists
        current['son_block'] = []
        current['parent_block'] = []
        current['same-name_block'] = []
        current['siblings_block'] = []

        # Compare with every other dictionary in the list
        for other in insight_vis_list:
            if current['Block_index'] != other['Block_index']:  # Ensure not comparing the same dictionary
                # Common properties between current and other
                if current['Block_size'] == other['Block_size']:
                    if is_same_name_relationship(current['insight_location(header)'], other['insight_location(header)']):
                        current['same-name_block'].append(other['Block_index'])
                    if is_siblings_relationship(current['insight_location(header)'], other['insight_location(header)']):
                        current['siblings_block'].append(other['Block_index'])

                # Check conditions for son_block and parent_block relationships
                if other['Block_size'] == current['Block_size'] + 1:
                    if is_valid_relationship(current['insight_location(header)'], other['insight_location(header)']):
                        current['son_block'].append(other['Block_index'])
                if other['Block_size'] == current['Block_size'] - 1:
                    if is_valid_relationship(other['insight_location(header)'], current['insight_location(header)']):
                        current['parent_block'].append(other['Block_index'])

    return insight_vis_list

def is_same_name_relationship(current_loc, other_loc):
    curr_loc1, curr_loc2 = current_loc
    other_loc1, other_loc2 = other_loc
    return (curr_loc1 == other_loc1 and curr_loc2[-1] == other_loc2[-1]) or (curr_loc2 == other_loc2 and curr_loc1[-1] == other_loc1[-1])

def is_siblings_relationship(current_loc, other_loc):
    curr_loc1, curr_loc2 = current_loc
    other_loc1, other_loc2 = other_loc
    return (curr_loc1 == other_loc1 and curr_loc2[:-1] == other_loc2[:-1] and curr_loc2[-1] != other_loc2[-1]) or \
           (curr_loc2 == other_loc2 and curr_loc1[:-1] == other_loc1[:-1] and curr_loc1[-1] != other_loc1[-1])

def is_valid_relationship(current_loc, other_loc):
    """ Helper function to determine valid relationships based on insight_location """
    curr_loc1, curr_loc2 = current_loc
    other_loc1, other_loc2 = other_loc
    # Check if one pair of tuples is identical and the other is a subset or superset
    return (curr_loc1 == other_loc1 and set(curr_loc2).issubset(set(other_loc2))) or \
           (curr_loc2 == other_loc2 and set(curr_loc1).issubset(set(other_loc1)))
    
def cal_block_size(header):
    x=header[0]
    y=header[1]
    return len(x)+len(y)

# 先写个假的
def header2location(header):
    x=header[0]
    y=header[1]
    up,down,left,right=0,0,0,0
    a=tuple()  
    if(x==a):
        up=3
        down=42
    if(len(x)==1):
        if x==('Nintendo',):
            up=3
            down=22
        if x==('Sony',):
            up=23
            down=34
        if x==('Microsoft',):
            up=35
            down=42
    if(len(x)==2):
        if x==('Nintendo','Nintendo 3DS (3DS)'):
            up=3
            down=6
        if x==('Nintendo','Nintendo DS (DS)'):
            up=7
            down=10
        if x==('Nintendo','Nintendo Switch (NS)'):
            up=11
            down=14
        if x==('Nintendo','Wii (Wii)'):
            up=15
            down=18
        if x==('Nintendo','Wii U (WiiU)'):
            up=19
            down=22                             
        if x==('Sony','PlayStation 3 (PS3)'):
            up=23
            down=26
        if x==('Sony','PlayStation 4 (PS4)'):
            up=27
            down=30        
        if x==('Sony','PlayStation Vita (PSV)'):
            up=31
            down=34                  
        if x==('Microsoft','Xbox 360 (X360)'):
            up=35
            down=38 
        if x==('Microsoft','Xbox 360 (X360)'):
            up=39
            down=42
            
    if(len(x)==3):
        if x==('Nintendo','Nintendo 3DS (3DS)','Europe'):
            up=3
            down=3
        if x==('Nintendo','Nintendo 3DS (3DS)','Japan'):
            up=4
            down=4        
        if x==('Nintendo','Nintendo 3DS (3DS)','North America'):
            up=5
            down=5            
        if x==('Nintendo','Nintendo 3DS (3DS)','Other'):
            up=6
            down=6           
        if x==('Nintendo','Nintendo DS (DS)','Europe'):
            up=7
            down=7
        if x==('Nintendo','Nintendo DS (DS)','Japan'):
            up=8
            down=8   
        if x==('Nintendo','Nintendo DS (DS)','North America'):
            up=9
            down=9    
        if x==('Nintendo','Nintendo DS (DS)','Other'):
            up=10
            down=10        
        if x==('Nintendo','Nintendo Switch (NS)','Europe'):
            up=11
            down=11
        if x==('Nintendo','Nintendo Switch (NS)','Japan'):
            up=12
            down=12    
        if x==('Nintendo','Nintendo Switch (NS)','North America'):
            up=13
            down=13    
        if x==('Nintendo','Nintendo Switch (NS)','Other'):
            up=14
            down=14       
        if x==('Nintendo','Wii (Wii)','Europe'):
            up=15
            down=15
        if x==('Nintendo','Wii (Wii)','Japan'):
            up=16
            down=16
        if x==('Nintendo','Wii (Wii)','North America'):
            up=17
            down=17    
        if x==('Nintendo','Wii (Wii)','Other'):
            up=18
            down=18    
        if x==('Nintendo','Wii U (WiiU)','Europe'):
            up=19
            down=19   
        if x==('Nintendo','Wii U (WiiU)','Japan'):
            up=20
            down=20             
        if x==('Nintendo','Wii U (WiiU)','North America'):
            up=21
            down=21             
        if x==('Nintendo','Wii U (WiiU)','Other'):
            up=22
            down=22                                      
        if x==('Sony','PlayStation 3 (PS3)','Europe'):
            up=23
            down=23
        if x==('Sony','PlayStation 3 (PS3)','Japan'):
            up=24
            down=24    
        if x==('Sony','PlayStation 3 (PS3)','North America'):
            up=25
            down=25    
        if x==('Sony','PlayStation 3 (PS3)','Other'):
            up=26
            down=26           
        if x==('Sony','PlayStation 4 (PS4)','Europe'):
            up=27
            down=37  
        if x==('Sony','PlayStation 4 (PS4)','Japan'):
            up=28
            down=28
        if x==('Sony','PlayStation 4 (PS4)','North America'):
            up=29
            down=29    
        if x==('Sony','PlayStation 4 (PS4)','Other'):
            up=30
            down=30                 
        if x==('Sony','PlayStation Vita (PSV)','Europe'):
            up=31
            down=31  
        if x==('Sony','PlayStation Vita (PSV)','Japan'):
            up=32
            down=32            
        if x==('Sony','PlayStation Vita (PSV)','North America'):
            up=33
            down=33             
        if x==('Sony','PlayStation Vita (PSV)','Other'):
            up=34
            down=34                                        
        if x==('Microsoft','Xbox 360 (X360)','Europe'):
            up=35
            down=35 
        if x==('Microsoft','Xbox 360 (X360)','Japan'):
            up=36
            down=36             
        if x==('Microsoft','Xbox 360 (X360)','North America'):
            up=37
            down=37             
        if x==('Microsoft','Xbox 360 (X360)','Other'):
            up=38
            down=38            
        if x==('Microsoft','Xbox 360 (X360)','Europe'):
            up=39
            down=39                   
        if x==('Microsoft','Xbox 360 (X360)','Japan'):
            up=40
            down=40              
        if x==('Microsoft','Xbox 360 (X360)','North America'):
            up=41
            down=41              
        if x==('Microsoft','Xbox 360 (X360)','Other'):
            up=42
            down=42 
            
     
    if(y==a):
        left=3
        right=22   
    if(len(y)==1):
        if y==('2013',):
            left=3
            right=6 
        if y==('2014',):
            left=7
            right=10             
        if y==('2015',):
            left=11
            right=14             
        if y==('2016',):
            left=15
            right=18 
        if y==('2017',):
            left=19
            right=22 
    if(len(y)==2):
        if y==('2013','MAR'):
            left=3
            right=3 
        if y==('2013','JUN'):
            left=4
            right=4     
        if y==('2013','SEP'):
            left=5
            right=5     
        if y==('2013','DEC'):
            left=6
            right=6      
        if y==('2014','MAR'):
            left=7
            right=7
        if y==('2014','JUN'):
            left=8
            right=8
        if y==('2014','SEP'):
            left=9
            right=9
        if y==('2014','DEC'):
            left=10
            right=10                 
        if y==('2015','MAR'):
            left=11
            right=11
        if y==('2015','JUN'):
            left=12
            right=12    
        if y==('2015','SEP'):
            left=13
            right=13
        if y==('2015','DEC'):
            left=14
            right=14                
        if y==('2016','MAR'):
            left=15
            right=15 
        if y==('2016','JUN'):
            left=16
            right=16 
        if y==('2016','SEP'):
            left=17
            right=17 
        if y==('2016','DEC'):
            left=18
            right=18 
        if y==('2017','MAR'):
            left=19
            right=19 
        if y==('2017','JUN'):
            left=20
            right=20                  
        if y==('2017','SEP'):
            left=21
            right=21 
        if y==('2017','DEC'):
            left=22
            right=22             
    up=up-1
    down=down-1
    return [up,down,left,right]       
            
            
            
            
            
            
            
            
            
                        
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            