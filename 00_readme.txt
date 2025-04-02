### Listar los parámetros disponibles
v4l2-ctl --list-ctrls

### Resetear a values por defecto
v4l2-ctl --set-ctrl=brightness=0
v4l2-ctl --set-ctrl=contrast=32
v4l2-ctl --set-ctrl=saturation=65
v4l2-ctl --set-ctrl=hue=0
v4l2-ctl --set-ctrl=white_balance_automatic=1
v4l2-ctl --set-ctrl=gamma=100
v4l2-ctl --set-ctrl=gain=0
v4l2-ctl --set-ctrl=power_line_frequency=2
v4l2-ctl --set-ctrl=sharpness=3
v4l2-ctl --set-ctrl=backlight_compensation=30
v4l2-ctl --set-ctrl=exposure_time_absolute=157
v4l2-ctl --set-ctrl=auto_exposure=3
v4l2-ctl --set-ctrl=exposure_dynamic_framerate=0

tmux ls
tmux kill-session -t 0

###################################################################################

tmux new -s nombre    	                Crear una nueva sesión
python3 start.py                          Lanza tu script
Ctrl + B, luego sueltas y pulsas D        Deja todo funcionando en segundo plano
tmux ls	                                Listar sesiones activas
tmux attach -t nombre	                    Reanudar una sesión
tmux kill-session -t nombre	            Cerrar una sesión