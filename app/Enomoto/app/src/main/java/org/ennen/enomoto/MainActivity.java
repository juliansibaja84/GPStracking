package org.ennen.enomoto;

import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.Toolbar;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.ListView;

import java.util.ArrayList;

public class MainActivity extends AppCompatActivity {

    private ArrayList<String> elements_to_record = new ArrayList<>();
    private int info_bar_status = 0;
    private Snackbar info;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.task_selector);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        elements_to_record.add("Android");
        elements_to_record.add("IPhone");
        elements_to_record.add("WindowsMobile");
        elements_to_record.add("Blackberry");
        elements_to_record.add("WebOS");
        elements_to_record.add("Ubuntu");
        elements_to_record.add("Windows7");
        elements_to_record.add("Max OS X");
        elements_to_record.add("Arch Linux");
        elements_to_record.add("Elementary OS");
        elements_to_record.add("Gentoo");
        elements_to_record.add("Nginx");
        elements_to_record.add("Django");
        elements_to_record.add("Tensor Flow");
        elements_to_record.add("Python");
        elements_to_record.add("Haskell");
        elements_to_record.add("Ennen");
        elements_to_record.add("Trovador");

        CustomListMember adapter = new CustomListMember(elements_to_record, this);

        ListView listView = (ListView) findViewById(R.id.tracking_list);
        listView.setAdapter(adapter);

        FloatingActionButton fab = (FloatingActionButton) findViewById(R.id.fab);
        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(info_bar_status == 0) {
                    info = Snackbar.make(view, "No OBD-II adapter Found, please check Bluetooth connection", Snackbar.LENGTH_INDEFINITE);
                    info.setAction("Action", null).show();
                    info_bar_status = 1;
                }
                else {
                    info.setAction("Action", null).dismiss();
                    info_bar_status = 0;
                }
            }
        });
    }
}
