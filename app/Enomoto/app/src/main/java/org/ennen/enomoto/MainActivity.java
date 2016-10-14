package org.ennen.enomoto;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.ArrayAdapter;
import android.widget.ListView;

import java.util.ArrayList;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        ArrayList<String> elements_to_record = new ArrayList<>();
        elements_to_record.add(0, "hola");
        String[] mobileArray = {"Android","IPhone","WindowsMobile","Blackberry","WebOS","Ubuntu","Windows7","Max OS X", "Android","IPhone","WindowsMobile","Blackberry","WebOS","Ubuntu","Windows7","Max OS X"};
        ArrayAdapter adapter = new ArrayAdapter<String>(this, R.layout.list_item, mobileArray);

        ListView listView = (ListView) findViewById(R.id.tracking_list);
        listView.setAdapter(adapter);
    }
}
