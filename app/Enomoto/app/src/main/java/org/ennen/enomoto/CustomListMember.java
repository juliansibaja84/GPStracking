package org.ennen.enomoto;

import android.content.Context;
import android.graphics.drawable.Drawable;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.ListAdapter;
import android.widget.TextView;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

/**
 * Created by asmateus on 14/10/16.
 */

public class CustomListMember extends BaseAdapter implements ListAdapter {
    private ArrayList<String> list = new ArrayList<>();
    private Context context;
    private final Map<String, Integer> ICON_CASES = new HashMap<String, Integer>();
    private final Map<String, Integer> ID_CASES = new HashMap<String, Integer>();

    private TaskSpawner tasky = new TaskSpawner();

    public CustomListMember(ArrayList<String> list, Context context) {
        // Fill ICON_CASES
        ICON_CASES.put("Trouble codes" , R.drawable.ic_trouble_code);
        ICON_CASES.put("Engine RPM" , R.drawable.ic_rpm);
        ICON_CASES.put("Engine load" , R.drawable.ic_e_load);
        ICON_CASES.put("Fuel pressure" , R.drawable.ic_f_pressure);
        ICON_CASES.put("Vehicle speed" , R.drawable.ic_speed);
        ICON_CASES.put("Throttle position" , R.drawable.ic_t_position);
        ICON_CASES.put("Time since engine start" , R.drawable.ic_time);
        ICON_CASES.put("Distance traveled" , R.drawable.ic_distance);
        ICON_CASES.put("Battery voltage" , R.drawable.ic_battery);

        // Fill ID_CASES
        ID_CASES.put("Trouble codes" , 1);
        ID_CASES.put("Engine RPM" , 2);
        ID_CASES.put("Engine load" , 3);
        ID_CASES.put("Fuel pressure" , 4);
        ID_CASES.put("Vehicle speed" , 5);
        ID_CASES.put("Throttle position" , 6);
        ID_CASES.put("Time since engine start" , 7);
        ID_CASES.put("Distance traveled" , 8);
        ID_CASES.put("Battery voltage" , 9);

        this.list = list;
        this.context = context;

        // Hide delete button on start
    }

    public void addItem(String task)
    {
        if(!this.list.contains(task)) {
            this.list.add(task);
            this.tasky.createTask(ID_CASES.get(task));
        }
    }

    @Override
    public int getCount() {
        return list.size();
    }

    @Override
    public Object getItem(int pos) {
        return list.get(pos);
    }

    @Override
    public long getItemId(int pos) {
        return 0;
        //return list.get(pos).getId();
        //just return 0 if your list items do not have an Id variable.
    }

    @Override
    public View getView(final int position, View convertView, ViewGroup parent) {
        View view = convertView;
        if (view == null) {
            LayoutInflater inflater = (LayoutInflater) context.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
            view = inflater.inflate(R.layout.list_item, null);
        }

        //Handle TextView and display string from your list
        TextView listItemText = (TextView)view.findViewById(R.id.list_item_string);
        ImageView img = (ImageView)view.findViewById(R.id.image_list);
        listItemText.setText(list.get(position));
        img.setImageResource(this.ICON_CASES.get(list.get(position)));

        //Handle buttons and add onClickListeners
        ImageButton deleteBtn = (ImageButton)view.findViewById(R.id.delete_btn);

        deleteBtn.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v) {
                //do something
                tasky.deleteTask(ID_CASES.get(position));
                list.remove(position); //or some other task
                notifyDataSetChanged();
            }
        });

        view.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v) {
                toogleButton(v);
            }
        });

        return view;
    }

    public void toogleButton(View v) {
        ImageButton btn = (ImageButton)v.findViewById(R.id.delete_btn);
        if(btn.getVisibility() == View.GONE) {
            btn.setClickable(true);
            btn.setVisibility(View.VISIBLE);
        }
        else {
            btn.setClickable(false);
            btn.setVisibility(View.GONE);
        }
    }
}
