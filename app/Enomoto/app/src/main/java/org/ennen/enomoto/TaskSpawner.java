package org.ennen.enomoto;

import android.bluetooth.BluetoothSocket;
import android.util.Log;

import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.concurrent.Executor;
import com.github.pires.obd.commands.protocol.*;
import com.github.pires.obd.commands.control.*;
import com.github.pires.obd.commands.engine.*;
import com.github.pires.obd.commands.pressure.*;
import com.github.pires.obd.commands.*;
import com.github.pires.obd.enums.ObdProtocols;

import java.util.Calendar;

/**
 * Created by asmateus on 15/10/16.
 */

public class TaskSpawner implements Executor
{
    ArrayList<Task> tasks = new ArrayList<Task>();
    MainActivity master;

    public TaskSpawner(MainActivity master)
    {
        this.master = master;
    }

    @Override
    public void execute(Runnable r)
    {
        Log.d("tasking", "CREATING NEW TASK");
        new Thread(r).start();
    }

    public void createTask(int task_id)
    {
        int i = 0;
        if(this.tasks.isEmpty()) {
            tasks.add(new Task(task_id));
            execute(tasks.get(tasks.size() - 1));
        }
        else {
            while(i < this.tasks.size() && this.tasks.get(i).task_id != task_id) ++i;
            if(i == this.tasks.size()) {
                tasks.add(new Task(task_id));
                execute(tasks.get(tasks.size() - 1));
            }
        }
    }

    public void deleteTask(int task_id)
    {
        int i = 0;
        while(i < this.tasks.size() && this.tasks.get(i).task_id != task_id) ++i;
        if(i != this.tasks.size()) {
            this.tasks.get(i).stop();
            this.tasks.remove(i);
        }
    }

    private class Task implements Runnable
    {
        private boolean shutdown = false;
        private final TroubleCodesCommand TR_CMD = new TroubleCodesCommand();
        private final RPMCommand RPM_CMD = new RPMCommand();
        private final LoadCommand LD_CMD = new LoadCommand();
        private final FuelPressureCommand F_PR_CMD = new FuelPressureCommand();
        private final SpeedCommand SP_CMD = new SpeedCommand();
        private final ThrottlePositionCommand THR_CMD = new ThrottlePositionCommand();
        private final RuntimeCommand RUN_T_CMD = new RuntimeCommand();
        private final DistanceSinceCCCommand DIS_CMD = new DistanceSinceCCCommand();
        private final ModuleVoltageCommand VOL_CMD = new ModuleVoltageCommand();

        public int task_id;
        public Task(int task_id)
        {
            this.task_id = task_id;
        }

        @Override
        public void run()
        {
            while(!shutdown) {
                if(master.bl_conn != null && master.bl_conn.conn_status == true) {
                    try {
                        Log.d("tasking2", "HELLO FROM TASK " + task_id);
                        initializeOBD(master.bl_conn.getSocket());
                        queryOBD(task_id);
                    }
                    catch (Exception e) {}
                }
                try {
                    Thread.sleep(3000);
                }
                catch (Exception e) {}
            }
        }

        public void stop()
        {
            this.shutdown = true;
        }

        private void initializeOBD(BluetoothSocket socket) throws Exception
        {
            // Init Configuration Commands
            new EchoOffCommand().run(socket.getInputStream(), socket.getOutputStream());
            new LineFeedOffCommand().run(socket.getInputStream(), socket.getOutputStream());
            new TimeoutCommand(125).run(socket.getInputStream(), socket.getOutputStream());
            new SelectProtocolCommand(ObdProtocols.AUTO).run(socket.getInputStream(), socket.getOutputStream());
        }

        private void queryOBD(int id) throws Exception
        {
            String result = "";

            switch (id) {
                case 1:
                    TR_CMD.run(master.bl_conn.getSocket().getInputStream(), master.bl_conn.getSocket().getOutputStream());
                    result = TR_CMD.getFormattedResult();
                    break;
                case 2:
                    RPM_CMD.run(master.bl_conn.getSocket().getInputStream(), master.bl_conn.getSocket().getOutputStream());
                    result = RPM_CMD.getFormattedResult();
                    break;
                case 3:
                    LD_CMD.run(master.bl_conn.getSocket().getInputStream(), master.bl_conn.getSocket().getOutputStream());
                    result = LD_CMD.getFormattedResult();
                    break;
                case 4:
                    F_PR_CMD.run(master.bl_conn.getSocket().getInputStream(), master.bl_conn.getSocket().getOutputStream());
                    result = F_PR_CMD.getFormattedResult();
                    break;
                case 5:
                    SP_CMD.run(master.bl_conn.getSocket().getInputStream(), master.bl_conn.getSocket().getOutputStream());
                    result = SP_CMD.getFormattedResult();
                    break;
                case 6:
                    THR_CMD.run(master.bl_conn.getSocket().getInputStream(), master.bl_conn.getSocket().getOutputStream());
                    result = THR_CMD.getFormattedResult();
                    break;
                case 7:
                    RUN_T_CMD.run(master.bl_conn.getSocket().getInputStream(), master.bl_conn.getSocket().getOutputStream());
                    result = RUN_T_CMD.getFormattedResult();
                    break;
                case 8:
                    DIS_CMD.run(master.bl_conn.getSocket().getInputStream(), master.bl_conn.getSocket().getOutputStream());
                    result = DIS_CMD.getFormattedResult();
                    break;
                case 9:
                    VOL_CMD.run(master.bl_conn.getSocket().getInputStream(), master.bl_conn.getSocket().getOutputStream());
                    result = VOL_CMD.getFormattedResult();
                    break;
            }

            DateFormat df = new SimpleDateFormat("dd-MM-yyyy_HH:mm:ss");
            Calendar c = Calendar.getInstance();
            master.collected_info_stack.push("taskid=" + id + "&datetime=" + df.format(c.getTime()) + "&val=" + result);
        }
    }
}
