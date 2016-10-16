package org.ennen.enomoto;

import android.content.Intent;
import android.graphics.drawable.Drawable;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.NavigationView;
import android.support.design.widget.Snackbar;
import android.support.v4.view.GravityCompat;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.Toast;

import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Stack;

public class MainActivity extends AppCompatActivity implements NavigationView.OnNavigationItemSelectedListener
{

    private ArrayList<String> elements_to_record = new ArrayList<>();
    private int info_bar_status = 0;
    private Snackbar info;
    private static final int REQUEST_CONNECT_DEVICE_SECURE = 1;

    public BluetoothConnector bl_conn;
    public boolean server_conn_status = false;
    public Stack<String> collected_info_stack = new Stack();

    // Main panel list
    private CustomListMember adapter = new CustomListMember(elements_to_record, this, this);

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.task_selector);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        ListView listView = (ListView) findViewById(R.id.tracking_list);
        listView.setAdapter(adapter);

        FloatingActionButton fab = (FloatingActionButton) findViewById(R.id.fab);
        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(info_bar_status == 0) {
                    String mess = buildInfoMessage();
                    info = Snackbar.make(view, mess, Snackbar.LENGTH_INDEFINITE);
                    info.setAction("Action", null).show();
                    info_bar_status = 1;
                }
                else {
                    info.setAction("Action", null).dismiss();
                    info_bar_status = 0;
                }
            }
        });

        NavigationView navigationView = (NavigationView) findViewById(R.id.nav_view);
        navigationView.setNavigationItemSelectedListener(this);

        // Init server connection
        ServerConnector server_connection = new ServerConnector("ennen.org", 80, this);
    }

    @Override
    public void onBackPressed() {
        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        if (drawer.isDrawerOpen(GravityCompat.START)) {
            drawer.closeDrawer(GravityCompat.START);
        } else {
            super.onBackPressed();
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.task_selector, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.secure_connect_scan) {
            bl_conn = new BluetoothConnector(this);
            Log.d("BL_CONN", "Conn status " + bl_conn.blStatus());
            //Intent obd_conn_intent = new Intent(this.getParent(), DeviceListActivity.class);
            //startActivityForResult(obd_conn_intent, REQUEST_CONNECT_DEVICE_SECURE);
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    @SuppressWarnings("StatementWithEmptyBody")
    @Override
    public boolean onNavigationItemSelected(MenuItem item) {
        // Handle navigation view item clicks here.
        int id = item.getItemId();
        String task_title = "";

        if (id == R.id.t_codes) {
            task_title = "Trouble codes";
        }
        else if (id == R.id.e_rpm) {
            task_title = "Engine RPM";
        }
        else if (id == R.id.e_load) {
            task_title = "Engine load";
        }
        else if (id == R.id.f_pressure) {
            task_title = "Fuel pressure";
        }
        else if (id == R.id.v_speed) {
            task_title = "Vehicle speed";
        }
        else if (id == R.id.t_position) {
            task_title = "Throttle position";
        }
        else if (id == R.id.t_e_start) {
            task_title = "Time since engine start";
        }
        else if (id == R.id.t_distance) {
            task_title = "Distance traveled";
        }
        else if (id == R.id.batt_voltage) {
            task_title = "Battery voltage";
        }

        adapter.addItem(task_title);
        adapter.notifyDataSetChanged();

        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        drawer.closeDrawer(GravityCompat.START);
        return true;
    }

    private String buildInfoMessage()
    {
        String mess = "";
        if(server_conn_status == false) {
            return "Can not connect to ennen.org";
        }

        if(this.elements_to_record.size() == 0)
            mess += "No Tasks selected to track\n";
        else
            mess += "Tracking " + this.elements_to_record.size() + " Tasks\n";

        if(!getOBDConnectionState())
            mess += "No OBD-II adapter found";
        else
            mess += "Device " + bl_conn.selected_device_MAC + " connected";

        return mess;
    }

    private boolean getOBDConnectionState()
    {
        if(this.bl_conn == null) return false;
        if(this.bl_conn.selected_device_MAC == "") return false;
        return this.bl_conn.conn_status;
    }
}
