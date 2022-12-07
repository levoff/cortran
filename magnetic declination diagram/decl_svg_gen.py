import math 
from math import atan, tan, sin, radians, degrees

def polar_to_cartesian(centerX, centerY, radius, angleInDegrees):
  angleInRadians = (angleInDegrees-90) * math.pi / 180.0;
  return {
    'x': centerX + (radius * math.cos(angleInRadians)),
    'y': centerY + (radius * math.sin(angleInRadians))
  }


def describe_arc(x, y, radius, startAngle, endAngle):
  start = polar_to_cartesian(x, y, radius, endAngle);
  end = polar_to_cartesian(x, y, radius, startAngle);
  largeArcFlag = "0" if endAngle - startAngle <= 180 else "1"
  negative = '1' if endAngle < startAngle else '0'
  return 'M %.1f,%.1f A %.1f,%.1f 0 %s,%s %.1f,%.1f '%( start['x'], start['y'], radius, radius, largeArcFlag, negative, end['x'], end['y']) 
   

def calc_converge(Lat, Long, CM=45):
  # γ = arctan [tan (λ - λ0) × sin φ]
  # γ is grid convergence, 
  # λ0 is longitude of UTM zone's central meridian, 
  # φ, λ are latitude, longitude of point in question
  ydd = atan(tan(radians(Long - CM)) * sin(radians(Lat)))
  return degrees(ydd)



print(round(calc_converge(39.98554, 45.98328)*60))


grid_angle= -1
magnetic_declination= 6.52
magnetic_declination_DM = str(int(magnetic_declination))+ '°' + str(abs(int((magnetic_declination-int(magnetic_declination))*60))) + '´'

if -2 < grid_angle < 2:
  grid_angle = 2 if grid_angle > 0 else -2

if -5 < magnetic_declination < 5:
  magnetic_declination = 5 if magnetic_declination > 0 else -5

grid_arc=describe_arc(x=0, y=200, radius=168, startAngle=0, endAngle=grid_angle)
magnetic_arc=describe_arc(x=0, y=200, radius=150, startAngle=0, endAngle=magnetic_declination)



f = open("decl.svg", "w")
f.write(f'''
<svg width="200" height="200" viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg">

    <rect x="1" y="1" width="199" height="199" fill="none" stroke="grey" stroke-width="1" />
    <g stroke="black" stroke-width="1" stroke-linecap="round" font-family="Verdana" font-size="12" transform="translate(100)">
        
        <g id="Gridline">
          <line x1="0" y1="200" x2="0" y2="30" transform="rotate({grid_angle} 10 200)" />
          <line x1="0" y1="30" x2="4" y2="23" transform="rotate({grid_angle} 10 200)" />
          <line x1="0" y1="30" x2="-4" y2="23" transform="rotate({grid_angle} 10 200)" />
        </g>
        <path d="{grid_arc}" stroke-dasharray="2,2" style="fill:none; stroke:blue; stroke-width:1"/>


        <g id="True">
          <line x1="0" y1="200" x2="0" y2="20"/>
          <polygon points="10,1 4,19.8 19,7.8 1,7.8 16,19.8" fill="black" transform="translate(-10)"/>
        </g>

        <g id="Magnetic" transform="rotate({magnetic_declination} 10 200)">
            <polygon points="-3,10 0,0 3,10" fill="black" transform="translate(0 40)" />
            <line x1="0" y1="200" x2="0" y2="50" />
            <text x="3" y="80" transform="rotate({-magnetic_declination} 3 80)">{magnetic_declination_DM}</text>
        </g>
        <path d="{magnetic_arc}" stroke-dasharray="2,2" style="fill:none; stroke:red; stroke-width:1"/>

    </g>
</svg>
''')
f.close()
