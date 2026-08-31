#property copyright "TDI"
#property version   "1.00"
#property indicator_chart_window
#property indicator_plots 0

input int RefreshSeconds = 2;
input int StaleAfterSeconds = 90;

//+------------------------------------------------------------------+
//| Custom indicator initialization                                  |
//+------------------------------------------------------------------+
int OnInit()
{
   EventSetTimer(RefreshSeconds);

   string panel_name = "TDI_PANEL_BACKGROUND";

   ObjectCreate(
      0,
      panel_name,
      OBJ_RECTANGLE_LABEL,
      0,
      0,
      0
   );

   ObjectSetInteger(
      0,
      panel_name,
      OBJPROP_CORNER,
      CORNER_LEFT_UPPER
   );

   ObjectSetInteger(
      0,
      panel_name,
      OBJPROP_XDISTANCE,
      10
   );

   ObjectSetInteger(
      0,
      panel_name,
      OBJPROP_YDISTANCE,
      30
   );

   ObjectSetInteger(
      0,
      panel_name,
      OBJPROP_XSIZE,
      300
   );

   ObjectSetInteger(
      0,
      panel_name,
      OBJPROP_YSIZE,
      735
   );

   ObjectSetInteger(
      0,
      panel_name,
      OBJPROP_BGCOLOR,
      clrBlack
   );

   ObjectSetInteger(
      0,
      panel_name,
      OBJPROP_BORDER_COLOR,
      clrDimGray
   );
   string title_name = "TDI_PANEL_TITLE";

   ObjectCreate(
      0,
      title_name,
      OBJ_LABEL,
      0,
      0,
      0
   );

   ObjectSetInteger(
      0,
      title_name,
      OBJPROP_CORNER,
      CORNER_LEFT_UPPER
   );

   ObjectSetInteger(
      0,
      title_name,
      OBJPROP_XDISTANCE,
      25
   );

   ObjectSetInteger(
      0,
      title_name,
      OBJPROP_YDISTANCE,
      40
   );

   ObjectSetInteger(
      0,
      title_name,
      OBJPROP_COLOR,
      clrWhite
   );

   ObjectSetInteger(
      0,
      title_name,
      OBJPROP_FONTSIZE,
      13
   );
   ObjectSetString(
   0,
   title_name,
   OBJPROP_FONT,
   "Arial Bold"
   );
   ObjectSetString(
      0,
      title_name,
      OBJPROP_TEXT,
      "TDI LIVE - " + _Symbol
   );

      string decision_name = "TDI_DECISION";
   string preferred_name = "TDI_PREFERRED_SIDE";
   string target_name = "TDI_TARGET_SIDE";


   ObjectCreate(
      0, decision_name, OBJ_LABEL, 0, 0, 0
   );
   ObjectSetInteger(
      0, decision_name,
      OBJPROP_CORNER, CORNER_LEFT_UPPER
   );
   ObjectSetInteger(
      0, decision_name,
      OBJPROP_XDISTANCE, 25
   );
   ObjectSetInteger(
      0, decision_name,
      OBJPROP_YDISTANCE, 80
   );
   ObjectSetInteger(
      0, decision_name,
      OBJPROP_COLOR, clrWhite
   );
   ObjectSetInteger(
      0, decision_name,
      OBJPROP_FONTSIZE, 11
   );
   ObjectSetString(
      0, decision_name,
      OBJPROP_TEXT, "DECISION"
   );

   ObjectCreate(
      0, preferred_name, OBJ_LABEL, 0, 0, 0
   );
   ObjectSetInteger(
      0, preferred_name,
      OBJPROP_CORNER, CORNER_LEFT_UPPER
   );
   ObjectSetInteger(
      0, preferred_name,
      OBJPROP_XDISTANCE, 25
   );
   ObjectSetInteger(
      0, preferred_name,
      OBJPROP_YDISTANCE, 105
   );
   ObjectSetInteger(
      0, preferred_name,
      OBJPROP_COLOR, clrSilver
   );
   ObjectSetInteger(
      0, preferred_name,
      OBJPROP_FONTSIZE, 10
   );
   ObjectSetString(
      0, preferred_name,
      OBJPROP_TEXT, "Preferred side : —"
   );

   ObjectCreate(
      0, target_name, OBJ_LABEL, 0, 0, 0
   );
   ObjectSetInteger(
      0, target_name,
      OBJPROP_CORNER, CORNER_LEFT_UPPER
   );
   ObjectSetInteger(
      0, target_name,
      OBJPROP_XDISTANCE, 25
   );
   ObjectSetInteger(
      0, target_name,
      OBJPROP_YDISTANCE, 130
   );
   ObjectSetInteger(
      0, target_name,
      OBJPROP_COLOR, clrSilver
   );
   ObjectSetInteger(
      0, target_name,
      OBJPROP_FONTSIZE, 10
   );
   ObjectSetString(
      0, target_name,
      OBJPROP_TEXT, "Target side    : —"
   );

      string bias_title_name = "TDI_BIAS_TITLE";
   string convergence_name = "TDI_BIAS_CONVERGENCE";
   string readiness_name = "TDI_BIAS_READINESS";
   string score_name = "TDI_BIAS_SCORE";

   CreateSectionSeparator(
      "TDI_SEPARATOR_BIAS",
      155
   );
   CreateSectionSeparator(
      "TDI_SEPARATOR_CONFIRMATION",
      270
   );
    CreateSectionSeparator(
      "TDI_SEPARATOR_SCENARIO",
      410
   );
   CreateSectionSeparator(
      "TDI_SEPARATOR_WAITING_FOR",
      500
   );
   CreateSectionSeparator(
      "TDI_SEPARATOR_TRANSITION",
      605
   );
   CreateSectionSeparator(
      "TDI_SEPARATOR_ALERT",
      670
   ObjectCreate(
      0, bias_title_name, OBJ_LABEL, 0, 0, 0
   );
   ObjectSetInteger(
      0, bias_title_name,
      OBJPROP_CORNER, CORNER_LEFT_UPPER
   );
   ObjectSetInteger(
      0, bias_title_name,
      OBJPROP_XDISTANCE, 25
   );
   ObjectSetInteger(
      0, bias_title_name,
      OBJPROP_YDISTANCE, 170
   );
   ObjectSetInteger(
      0, bias_title_name,
      OBJPROP_COLOR, clrWhite
   );
   ObjectSetInteger(
      0, bias_title_name,
      OBJPROP_FONTSIZE, 11
   );
   ObjectSetString(
      0, bias_title_name,
      OBJPROP_TEXT, "BIAS"
   );

   ObjectCreate(
      0, convergence_name, OBJ_LABEL, 0, 0, 0
   );
   ObjectSetInteger(
      0, convergence_name,
      OBJPROP_CORNER, CORNER_LEFT_UPPER
   );
   ObjectSetInteger(
      0, convergence_name,
      OBJPROP_XDISTANCE, 25
   );
   ObjectSetInteger(
      0, convergence_name,
      OBJPROP_YDISTANCE, 195
   );
   ObjectSetInteger(
      0, convergence_name,
      OBJPROP_COLOR, clrSilver
   );
   ObjectSetInteger(
      0, convergence_name,
      OBJPROP_FONTSIZE, 10
   );
   ObjectSetString(
      0, convergence_name,
      OBJPROP_TEXT, "Convergence : —"
   );

   ObjectCreate(
      0, readiness_name, OBJ_LABEL, 0, 0, 0
   );
   ObjectSetInteger(
      0, readiness_name,
      OBJPROP_CORNER, CORNER_LEFT_UPPER
   );
   ObjectSetInteger(
      0, readiness_name,
      OBJPROP_XDISTANCE, 25
   );
   ObjectSetInteger(
      0, readiness_name,
      OBJPROP_YDISTANCE, 220
   );
   ObjectSetInteger(
      0, readiness_name,
      OBJPROP_COLOR, clrSilver
   );
   ObjectSetInteger(
      0, readiness_name,
      OBJPROP_FONTSIZE, 10
   );
   ObjectSetString(
      0, readiness_name,
      OBJPROP_TEXT, "Readiness   : —"
   );

   ObjectCreate(
      0, score_name, OBJ_LABEL, 0, 0, 0
   );
   ObjectSetInteger(
      0, score_name,
      OBJPROP_CORNER, CORNER_LEFT_UPPER
   );
   ObjectSetInteger(
      0, score_name,
      OBJPROP_XDISTANCE, 25
   );
   ObjectSetInteger(
      0, score_name,
      OBJPROP_YDISTANCE, 245
   );
   ObjectSetInteger(
      0, score_name,
      OBJPROP_COLOR, clrSilver
   );
   ObjectSetInteger(
      0, score_name,
      OBJPROP_FONTSIZE, 10
   );
   ObjectSetString(
      0, score_name,
      OBJPROP_TEXT, "Score       : —/100"
   );

      string scenario_title_name = "TDI_SCENARIO_TITLE";
   string scenario_state_name = "TDI_SCENARIO_STATE";
   string scenario_score_name = "TDI_SCENARIO_SCORE";

   ObjectCreate(
      0, scenario_title_name, OBJ_LABEL, 0, 0, 0
   );
   ObjectSetInteger(
      0, scenario_title_name,
      OBJPROP_CORNER, CORNER_LEFT_UPPER
   );
   ObjectSetInteger(
      0, scenario_title_name,
      OBJPROP_XDISTANCE, 25
   );
   ObjectSetInteger(
      0, scenario_title_name,
      OBJPROP_YDISTANCE, 425
   );
   ObjectSetInteger(
      0, scenario_title_name,
      OBJPROP_COLOR, clrWhite
   );
   ObjectSetInteger(
      0, scenario_title_name,
      OBJPROP_FONTSIZE, 11
   );
   ObjectSetString(
      0, scenario_title_name,
      OBJPROP_TEXT, "SCENARIO"
   );

   ObjectCreate(
      0, scenario_state_name, OBJ_LABEL, 0, 0, 0
   );
   ObjectSetInteger(
      0, scenario_state_name,
      OBJPROP_CORNER, CORNER_LEFT_UPPER
   );
   ObjectSetInteger(
      0, scenario_state_name,
      OBJPROP_XDISTANCE, 25
   );
   ObjectSetInteger(
      0, scenario_state_name,
      OBJPROP_YDISTANCE, 450
      );
   ObjectSetInteger(
      0, scenario_state_name,
      OBJPROP_COLOR, clrSilver
   );
   ObjectSetInteger(
      0, scenario_state_name,
      OBJPROP_FONTSIZE, 10
   );
   ObjectSetString(
      0, scenario_state_name,
      OBJPROP_TEXT, "State : —"
   );

   ObjectCreate(
      0, scenario_score_name, OBJ_LABEL, 0, 0, 0
   );
   ObjectSetInteger(
      0, scenario_score_name,
      OBJPROP_CORNER, CORNER_LEFT_UPPER
   );
   ObjectSetInteger(
      0, scenario_score_name,
      OBJPROP_XDISTANCE, 25
   );
   ObjectSetInteger(
      0, scenario_score_name,
      OBJPROP_YDISTANCE, 475
   );
   ObjectSetInteger(
      0, scenario_score_name,
      OBJPROP_COLOR, clrSilver
   );
   ObjectSetInteger(
      0, scenario_score_name,
      OBJPROP_FONTSIZE, 10
   );
   ObjectSetString(
      0, scenario_score_name,
      OBJPROP_TEXT, "Score : —/100"
   );

      string confirmation_title_name = "TDI_CONFIRMATION_TITLE";
   string bias_aligned_name = "TDI_CONFIRMATION_BIAS";
   string structure_aligned_name = "TDI_CONFIRMATION_STRUCTURE";
   string timing_favorable_name = "TDI_CONFIRMATION_TIMING";
   string momentum_confirmed_name = "TDI_CONFIRMATION_MOMENTUM";

   ObjectCreate(
      0, confirmation_title_name, OBJ_LABEL, 0, 0, 0
   );
   ObjectSetInteger(
      0, confirmation_title_name,
      OBJPROP_CORNER, CORNER_LEFT_UPPER
   );
   ObjectSetInteger(
      0, confirmation_title_name,
      OBJPROP_XDISTANCE, 25
   );
   ObjectSetInteger(
      0, confirmation_title_name,
      OBJPROP_YDISTANCE, 285
   );
   ObjectSetInteger(
      0, confirmation_title_name,
      OBJPROP_COLOR, clrWhite
   );
   ObjectSetInteger(
      0, confirmation_title_name,
      OBJPROP_FONTSIZE, 11
   );
   ObjectSetString(
      0, confirmation_title_name,
      OBJPROP_TEXT, "CONFIRMATION"
   );

   ObjectCreate(
      0, bias_aligned_name, OBJ_LABEL, 0, 0, 0
   );
   ObjectSetInteger(
      0, bias_aligned_name,
      OBJPROP_CORNER, CORNER_LEFT_UPPER
   );
   ObjectSetInteger(
      0, bias_aligned_name,
      OBJPROP_XDISTANCE, 25
   );
   ObjectSetInteger(
      0, bias_aligned_name,
      OBJPROP_YDISTANCE, 310
   );
   ObjectSetInteger(
      0, bias_aligned_name,
      OBJPROP_COLOR, clrSilver
   );
   ObjectSetInteger(
      0, bias_aligned_name,
      OBJPROP_FONTSIZE, 10
   );
   ObjectSetString(
      0, bias_aligned_name,
      OBJPROP_TEXT, "Bias aligned      : —"
   );

   ObjectCreate(
      0, structure_aligned_name, OBJ_LABEL, 0, 0, 0
   );
   ObjectSetInteger(
      0, structure_aligned_name,
      OBJPROP_CORNER, CORNER_LEFT_UPPER
   );
   ObjectSetInteger(
      0, structure_aligned_name,
      OBJPROP_XDISTANCE, 25
   );
   ObjectSetInteger(
      0, structure_aligned_name,
      OBJPROP_YDISTANCE, 335
   );
   ObjectSetInteger(
      0, structure_aligned_name,
      OBJPROP_COLOR, clrSilver
   );
   ObjectSetInteger(
      0, structure_aligned_name,
      OBJPROP_FONTSIZE, 10
   );
   ObjectSetString(
      0, structure_aligned_name,
      OBJPROP_TEXT, "Structure aligned : —"
   );

   ObjectCreate(
      0, timing_favorable_name, OBJ_LABEL, 0, 0, 0
   );
   ObjectSetInteger(
      0, timing_favorable_name,
      OBJPROP_CORNER, CORNER_LEFT_UPPER
   );
   ObjectSetInteger(
      0, timing_favorable_name,
      OBJPROP_XDISTANCE, 25
   );
   ObjectSetInteger(
      0, timing_favorable_name,
      OBJPROP_YDISTANCE, 360
   );
   ObjectSetInteger(
      0, timing_favorable_name,
      OBJPROP_COLOR, clrSilver
   );
   ObjectSetInteger(
      0, timing_favorable_name,
      OBJPROP_FONTSIZE, 10
   );
   ObjectSetString(
      0, timing_favorable_name,
      OBJPROP_TEXT, "Timing favorable  : —"
   );

   ObjectCreate(
      0, momentum_confirmed_name, OBJ_LABEL, 0, 0, 0
   );
   ObjectSetInteger(
      0, momentum_confirmed_name,
      OBJPROP_CORNER, CORNER_LEFT_UPPER
   );
   ObjectSetInteger(
      0, momentum_confirmed_name,
      OBJPROP_XDISTANCE, 25
   );
   ObjectSetInteger(
      0, momentum_confirmed_name,
      OBJPROP_YDISTANCE, 385
   );
   ObjectSetInteger(
      0, momentum_confirmed_name,
      OBJPROP_COLOR, clrSilver
   );
   ObjectSetInteger(
      0, momentum_confirmed_name,
      OBJPROP_FONTSIZE, 10
   );
   ObjectSetString(
      0, momentum_confirmed_name,
      OBJPROP_TEXT, "Momentum confirmed: —"
   );

      string waiting_title_name = "TDI_WAITING_TITLE";
   string waiting_value_name = "TDI_WAITING_VALUE";

   ObjectCreate(
      0, waiting_title_name, OBJ_LABEL, 0, 0, 0
   );
   ObjectSetInteger(
      0, waiting_title_name,
      OBJPROP_CORNER, CORNER_LEFT_UPPER
   );
   ObjectSetInteger(
      0, waiting_title_name,
      OBJPROP_XDISTANCE, 25
   );
   ObjectSetInteger(
      0, waiting_title_name,
      OBJPROP_YDISTANCE, 515
   );
   ObjectSetInteger(
      0, waiting_title_name,
      OBJPROP_COLOR, clrWhite
   );
   ObjectSetInteger(
      0, waiting_title_name,
      OBJPROP_FONTSIZE, 11
   );
   ObjectSetString(
      0, waiting_title_name,
      OBJPROP_TEXT, "WAITING FOR"
   );

   ObjectCreate(
      0, waiting_value_name, OBJ_LABEL, 0, 0, 0
   );
   ObjectSetInteger(
      0, waiting_value_name,
      OBJPROP_CORNER, CORNER_LEFT_UPPER
   );
   ObjectSetInteger(
      0, waiting_value_name,
      OBJPROP_XDISTANCE, 25
   );
   ObjectSetInteger(
      0, waiting_value_name,
      OBJPROP_YDISTANCE, 540
   );
   ObjectSetInteger(
      0, waiting_value_name,
      OBJPROP_COLOR, clrSilver
   );
   ObjectSetInteger(
      0, waiting_value_name,
      OBJPROP_FONTSIZE, 10
   );
   string waiting_value_2_name = "TDI_WAITING_VALUE_2";

   ObjectCreate(
      0, waiting_value_2_name, OBJ_LABEL, 0, 0, 0
   );
   ObjectSetInteger(
      0, waiting_value_2_name,
      OBJPROP_CORNER, CORNER_LEFT_UPPER
   );
   ObjectSetInteger(
      0, waiting_value_2_name,
      OBJPROP_XDISTANCE, 25
   );
   ObjectSetInteger(
      0, waiting_value_2_name,
      OBJPROP_YDISTANCE, 560
   );
   ObjectSetInteger(
      0, waiting_value_2_name,
      OBJPROP_COLOR, clrSilver
   );
   ObjectSetInteger(
      0, waiting_value_2_name,
      OBJPROP_FONTSIZE, 10
   );
   ObjectSetString(
      0,
      waiting_value_2_name,
      OBJPROP_TEXT,
      "—"
   );

    string waiting_value_3_name = "TDI_WAITING_VALUE_3";

   ObjectCreate(
      0, waiting_value_3_name, OBJ_LABEL, 0, 0, 0
   );
   ObjectSetInteger(
      0, waiting_value_3_name,
      OBJPROP_CORNER, CORNER_LEFT_UPPER
   );
   ObjectSetInteger(
      0, waiting_value_3_name,
      OBJPROP_XDISTANCE, 25
   );
   ObjectSetInteger(
      0, waiting_value_3_name,
      OBJPROP_YDISTANCE, 580
   );
   ObjectSetInteger(
      0, waiting_value_3_name,
      OBJPROP_COLOR, clrSilver
   );
   ObjectSetInteger(
      0, waiting_value_3_name,
      OBJPROP_FONTSIZE, 10
   );
   ObjectSetString(
      0,
      waiting_value_3_name,
      OBJPROP_TEXT,
      "—"
   );
   ObjectSetString(
      0, waiting_value_name,
      OBJPROP_TEXT, "—"
   );

    string transition_title_name = "TDI_TRANSITION_TITLE";
   string transition_value_name = "TDI_TRANSITION_VALUE";

   ObjectCreate(
      0, transition_title_name, OBJ_LABEL, 0, 0, 0
   );
   ObjectSetInteger(
      0, transition_title_name,
      OBJPROP_CORNER, CORNER_LEFT_UPPER
   );
   ObjectSetInteger(
      0, transition_title_name,
      OBJPROP_XDISTANCE, 25
   );
   ObjectSetInteger(
      0, transition_title_name,
      OBJPROP_YDISTANCE, 620
   );
   ObjectSetInteger(
      0, transition_title_name,
      OBJPROP_COLOR, clrWhite
   );
   ObjectSetInteger(
      0, transition_title_name,
      OBJPROP_FONTSIZE, 11
   );
   ObjectSetString(
      0, transition_title_name,
      OBJPROP_TEXT, "TRANSITION"
   );

   ObjectCreate(
      0, transition_value_name, OBJ_LABEL, 0, 0, 0
   );
   ObjectSetInteger(
      0, transition_value_name,
      OBJPROP_CORNER, CORNER_LEFT_UPPER
   );
   ObjectSetInteger(
      0, transition_value_name,
      OBJPROP_XDISTANCE, 25
   );
   ObjectSetInteger(
      0, transition_value_name,
      OBJPROP_YDISTANCE, 645
   );
   ObjectSetInteger(
      0, transition_value_name,
      OBJPROP_COLOR, clrSilver
   );
   ObjectSetInteger(
      0, transition_value_name,
      OBJPROP_FONTSIZE, 10
   );
   ObjectSetString(
      0, transition_value_name,
      OBJPROP_TEXT, "—"
   );

      string alert_title_name = "TDI_ALERT_TITLE";
   string alert_level_name = "TDI_ALERT_LEVEL";
   string alert_active_name = "TDI_ALERT_ACTIVE";

   ObjectCreate(
      0, alert_title_name, OBJ_LABEL, 0, 0, 0
   );
   ObjectSetInteger(
      0, alert_title_name,
      OBJPROP_CORNER, CORNER_LEFT_UPPER
   );
   ObjectSetInteger(
      0, alert_title_name,
      OBJPROP_XDISTANCE, 25
   );
   ObjectSetInteger(
      0, alert_title_name,
      OBJPROP_YDISTANCE, 685
   );
   ObjectSetInteger(
      0, alert_title_name,
      OBJPROP_COLOR, clrWhite
   );
   ObjectSetInteger(
      0, alert_title_name,
      OBJPROP_FONTSIZE, 11
   );
   ObjectSetString(
      0, alert_title_name,
      OBJPROP_TEXT, "ALERT"
   );

   ObjectCreate(
      0, alert_level_name, OBJ_LABEL, 0, 0, 0
   );
   ObjectSetInteger(
      0, alert_level_name,
      OBJPROP_CORNER, CORNER_LEFT_UPPER
   );
   ObjectSetInteger(
      0, alert_level_name,
      OBJPROP_XDISTANCE, 25
   );
   ObjectSetInteger(
      0, alert_level_name,
      OBJPROP_YDISTANCE, 710
   );
   ObjectSetInteger(
      0, alert_level_name,
      OBJPROP_COLOR, clrSilver
   );
   ObjectSetInteger(
      0, alert_level_name,
      OBJPROP_FONTSIZE, 10
   );
   ObjectSetString(
      0, alert_level_name,
      OBJPROP_TEXT, "Level  : —"
   );

   ObjectCreate(
      0, alert_active_name, OBJ_LABEL, 0, 0, 0
   );
   ObjectSetInteger(
      0, alert_active_name,
      OBJPROP_CORNER, CORNER_LEFT_UPPER
   );
   ObjectSetInteger(
      0, alert_active_name,
      OBJPROP_XDISTANCE, 25
   );
   ObjectSetInteger(
      0, alert_active_name,
      OBJPROP_YDISTANCE, 735
   );
   ObjectSetInteger(
      0, alert_active_name,
      OBJPROP_COLOR, clrSilver
   );
   ObjectSetInteger(
      0, alert_active_name,
      OBJPROP_FONTSIZE, 10
   );
   ObjectSetString(
      0, alert_active_name,
      OBJPROP_TEXT, "Active : —"
   );

   ChartRedraw();

   Print("TDI Dashboard initialized for ", _Symbol);

   return(INIT_SUCCEEDED);
}
//+------------------------------------------------------------------+
//| Custom indicator deinitialization                                |
//+------------------------------------------------------------------+
void CreateSectionSeparator(
   string name,
   int y
)
{
   ObjectCreate(
      0,
      name,
      OBJ_RECTANGLE_LABEL,
      0,
      0,
      0
   );

   ObjectSetInteger(
      0, name,
      OBJPROP_CORNER, CORNER_LEFT_UPPER
   );
   ObjectSetInteger(
      0, name,
      OBJPROP_XDISTANCE, 20
   );
   ObjectSetInteger(
      0, name,
      OBJPROP_YDISTANCE, y
   );
   ObjectSetInteger(
      0, name,
      OBJPROP_XSIZE, 280
   );
   ObjectSetInteger(
      0, name,
      OBJPROP_YSIZE, 1
   );
   ObjectSetInteger(
      0, name,
      OBJPROP_BGCOLOR, clrDimGray
   );
   ObjectSetInteger(
      0, name,
      OBJPROP_BORDER_COLOR, clrDimGray
   );
}

void OnDeinit(const int reason)
{
   EventKillTimer();

   ObjectsDeleteAll(
      0,
      "TDI_"
   );

   ChartRedraw();

   Print("TDI Dashboard stopped for ", _Symbol);
}

//+------------------------------------------------------------------+
//| Timer                                                            |
//+------------------------------------------------------------------+
string JsonGetString(
   const string json,
   const string key
)
{
   string search = "\"" + key + "\":";

   int key_pos = StringFind(
      json,
      search
   );

   if(key_pos < 0)
      return("");

   int value_start = StringFind(
      json,
      "\"",
      key_pos + StringLen(search)
   );

   if(value_start < 0)
      return("");

   int value_end = StringFind(
      json,
      "\"",
      value_start + 1
   );

   if(value_end < 0)
      return("");

   return(
      StringSubstr(
         json,
         value_start + 1,
         value_end - value_start - 1
      )
   );
}

string JsonGetNullableString(
   const string json,
   const string key
)
{
   string search = "\"" + key + "\":";

   int key_pos = StringFind(
      json,
      search
   );

   if(key_pos < 0)
      return("—");

   int null_pos = StringFind(
      json,
      "null",
      key_pos + StringLen(search)
   );

   int quote_pos = StringFind(
      json,
      "\"",
      key_pos + StringLen(search)
   );

   if(
      null_pos >= 0
      && (quote_pos < 0 || null_pos < quote_pos)
   )
      return("—");

   return(
      JsonGetString(
         json,
         key
      )
   );
}

int JsonGetInt(
   const string json,
   const string key
)
{
   string search = "\"" + key + "\":";

   int key_pos = StringFind(
      json,
      search
   );

   if(key_pos < 0)
      return(0);

   int start = key_pos + StringLen(search);

   while(
      start < StringLen(json)
      && StringGetCharacter(json, start) == ' '
   )
   {
      start++;
   }

   string value = "";

   while(start < StringLen(json))
   {
      ushort c = StringGetCharacter(json, start);

      if(c < '0' || c > '9')
         break;

      value += ShortToString(c);
      start++;
   }

   return((int)StringToInteger(value));
}

string JsonGetBool(
   const string json,
   const string key
)
{
   string search = "\"" + key + "\":";

   int key_pos = StringFind(
      json,
      search
   );

   if(key_pos < 0)
      return("—");

   int start = key_pos + StringLen(search);

   while(
      start < StringLen(json)
      && StringGetCharacter(json, start) == ' '
   )
   {
      start++;
   }

   if(
      StringSubstr(json, start, 4) == "true"
   )
      return("True");

   if(
      StringSubstr(json, start, 5) == "false"
   )
      return("False");

   return("—");
}

datetime IsoUtcToDatetime(
   const string iso_value
)
{
   if(StringLen(iso_value) < 19)
      return(0);

   string value = StringSubstr(
      iso_value,
      0,
      19
   );

   StringReplace(
      value,
      "-",
      "."
   );

   StringReplace(
      value,
      "T",
      " "
   );

   return(
      StringToTime(value)
   );
}





string JsonGetArrayStringAt(
   const string json,
   const string key,
   const int index
)
{
   string search = "\"" + key + "\":";

   int key_pos = StringFind(
      json,
      search
   );

   if(key_pos < 0)
      return("");

   int array_start = StringFind(
      json,
      "[",
      key_pos + StringLen(search)
   );

   if(array_start < 0)
      return("");

   int array_end = StringFind(
      json,
      "]",
      array_start + 1
   );

   if(array_end < 0)
      return("");

   int position = array_start + 1;
   int current_index = 0;

   while(position < array_end)
   {
      int value_start = StringFind(
         json,
         "\"",
         position
      );

      if(
         value_start < 0
         || value_start >= array_end
      )
         break;

      int value_end = StringFind(
         json,
         "\"",
         value_start + 1
      );

      if(
         value_end < 0
         || value_end > array_end
      )
         break;

      if(current_index == index)
      {
         return(
            StringSubstr(
               json,
               value_start + 1,
               value_end - value_start - 1
            )
         );
      }

      current_index++;
      position = value_end + 1;
   }

   return("");
}

void OnTimer()
{
   string file_name = _Symbol + ".json";

   int handle = FileOpen(
      file_name,
      FILE_READ | FILE_TXT | FILE_ANSI
   );

   if(handle == INVALID_HANDLE)
   {
      Print(
         "TDI Dashboard: cannot open ",
         file_name,
         " | error=",
         GetLastError()
      );
      return;
   }

   string content = "";

   while(!FileIsEnding(handle))
   {
      content += FileReadString(handle);
   }

   FileClose(handle);

     string decision = JsonGetString(
      content,
      "decision"
   );

      string preferred_side = JsonGetNullableString(
      content,
      "preferred_side"
   );

   string target_side = JsonGetNullableString(
      content,
      "target_side"
   );

      string bias_convergence = JsonGetString(
      content,
      "bias_convergence"
   );

   string bias_readiness = JsonGetString(
      content,
      "bias_readiness"
   );

   int bias_score = JsonGetInt(
      content,
      "bias_score"
   );

      string scenario_state = JsonGetString(
      content,
      "scenario"
   );

   int scenario_score = JsonGetInt(
      content,
      "scenario_score"
   );

      string waiting_for = JsonGetArrayStringAt(
         content,
         "waiting_for",
         0
      );

      string waiting_for_2 = JsonGetArrayStringAt(
         content,
         "waiting_for",
         1
      );

      string waiting_for_3 = JsonGetArrayStringAt(
         content,
         "waiting_for",
         2
      );

      if(waiting_for_2 == "")
         waiting_for_2 = " ";

      if(waiting_for_3 == "")
         waiting_for_3 = " ";

   string transition = JsonGetString(
   content,
   "transition"
   );

   string alert_level = JsonGetString(
      content,
      "alert_level"
   );

   string bias_aligned = JsonGetBool(
      content,
      "bias_aligned"
   );

   string structure_aligned = JsonGetBool(
      content,
      "structure_aligned"
   );

   string timing_favorable = JsonGetBool(
      content,
      "timing_favorable"
   );

   string momentum_confirmed = JsonGetBool(
      content,
      "momentum_confirmed"
   );

   string alert_active = JsonGetBool(
      content,
      "alert_active"
   );

   string updated_at = JsonGetString(
      content,
      "updated_at"
   );

   datetime updated_time = IsoUtcToDatetime(
      updated_at
   );

   long state_age_seconds = (
      updated_time > 0
      ? (long)(TimeGMT() - updated_time)
      : -1
   );

   bool is_stale = (
      state_age_seconds < 0
      || state_age_seconds > StaleAfterSeconds
   );

   if(is_stale)
   {
   ObjectSetString(
      0,
      "TDI_PANEL_TITLE",
      OBJPROP_TEXT,
      "TDI LIVE - "
      + _Symbol
      + "   |   STALE"
   );
      ObjectSetInteger(
      0,
      "TDI_PANEL_TITLE",
      OBJPROP_COLOR,
      clrTomato
   );
   }
   else
   {
   ObjectSetString(
      0,
      "TDI_PANEL_TITLE",
      OBJPROP_TEXT,
      "TDI LIVE - "
      + _Symbol
      + "   |   "
      + decision
   );
      ObjectSetInteger(
      0,
      "TDI_PANEL_TITLE",
      OBJPROP_COLOR,
      decision == "Buy"
      ? clrLimeGreen
      : decision == "Sell"
        ? clrTomato
        : clrWhite
   );
   }

      ObjectSetString(
      0,
      "TDI_PREFERRED_SIDE",
      OBJPROP_TEXT,
      "Preferred side : " + preferred_side
   );

   ObjectSetString(
      0,
      "TDI_TARGET_SIDE",
      OBJPROP_TEXT,
      "Target side    : " + target_side
   );

      ObjectSetString(
      0,
      "TDI_BIAS_CONVERGENCE",
      OBJPROP_TEXT,
      "Convergence : " + bias_convergence
   );

   ObjectSetString(
      0,
      "TDI_BIAS_READINESS",
      OBJPROP_TEXT,
      "Readiness   : " + bias_readiness
   );

   ObjectSetInteger(
      0,
      "TDI_BIAS_READINESS",
      OBJPROP_COLOR,
      StringFind(bias_readiness, "High") >= 0
      ? clrLimeGreen
      : StringFind(bias_readiness, "Medium") >= 0
        ? clrOrange
        : clrSilver
   );

   ObjectSetString(
      0,
      "TDI_BIAS_SCORE",
      OBJPROP_TEXT,
      "Score       : "
      + IntegerToString(bias_score)
      + "/100"
   );

   ObjectSetString(
      0,
      "TDI_CONFIRMATION_BIAS",
      OBJPROP_TEXT,
      "Bias aligned      : " + bias_aligned
   );

   ObjectSetInteger(
      0,
      "TDI_CONFIRMATION_BIAS",
      OBJPROP_COLOR,
      bias_aligned == "True"
      ? clrLimeGreen
      : clrSilver
   );

   ObjectSetString(
      0,
      "TDI_CONFIRMATION_STRUCTURE",
      OBJPROP_TEXT,
      "Structure aligned : " + structure_aligned
   );

   ObjectSetInteger(
      0,
      "TDI_CONFIRMATION_STRUCTURE",
      OBJPROP_COLOR,
      structure_aligned == "True"
      ? clrLimeGreen
      : clrSilver
   );

   ObjectSetString(
      0,
      "TDI_CONFIRMATION_TIMING",
      OBJPROP_TEXT,
      "Timing favorable  : " + timing_favorable
   );

   ObjectSetInteger(
      0,
      "TDI_CONFIRMATION_TIMING",
      OBJPROP_COLOR,
      timing_favorable == "True"
      ? clrLimeGreen
      : clrSilver
   );

   ObjectSetString(
      0,
      "TDI_CONFIRMATION_MOMENTUM",
      OBJPROP_TEXT,
      "Momentum confirmed: " + momentum_confirmed
   );

   ObjectSetInteger(
      0,
      "TDI_CONFIRMATION_MOMENTUM",
      OBJPROP_COLOR,
      momentum_confirmed == "True"
      ? clrLimeGreen
      : clrSilver
   );

   ObjectSetString(
      0,
      "TDI_SCENARIO_STATE",
      OBJPROP_TEXT,
      "State : " + scenario_state
   );

   ObjectSetInteger(
      0,
      "TDI_SCENARIO_STATE",
      OBJPROP_COLOR,
      StringFind(scenario_state, "Ready") >= 0
      ? clrLimeGreen
      : StringFind(scenario_state, "Building") >= 0
        ? clrOrange
        : StringFind(scenario_state, "Degrading") >= 0
          ? clrOrangeRed
          : clrSilver
   );

   ObjectSetString(
      0,
      "TDI_SCENARIO_SCORE",
      OBJPROP_TEXT,
      "Score : "
      + IntegerToString(scenario_score)
      + "/100"
   );

   ObjectSetString(
      0,
      "TDI_WAITING_VALUE",
      OBJPROP_TEXT,
      waiting_for
   );

   ObjectSetString(
      0,
      "TDI_WAITING_VALUE_2",
      OBJPROP_TEXT,
      waiting_for_2
   );

   ObjectSetString(
      0,
      "TDI_WAITING_VALUE_3",
      OBJPROP_TEXT,
      waiting_for_3
   );



   ObjectSetString(
      0,
      "TDI_TRANSITION_VALUE",
      OBJPROP_TEXT,
      transition
   );

   string alert_level_upper = alert_level;
   StringToUpper(alert_level_upper);

   ObjectSetString(
      0,
      "TDI_ALERT_LEVEL",
      OBJPROP_TEXT,
      "Level  : " + alert_level
   );

   ObjectSetInteger(
      0,
      "TDI_ALERT_LEVEL",
      OBJPROP_COLOR,
      StringFind(alert_level_upper, "HIGH") >= 0
      ? clrOrangeRed
      : StringFind(alert_level_upper, "WARNING") >= 0
        ? clrOrange
        : StringFind(alert_level_upper, "INFO") >= 0
          ? clrWhite
          : clrSilver
   );

   ObjectSetString(
      0,
      "TDI_ALERT_ACTIVE",
      OBJPROP_TEXT,
      "Active : " + alert_active
   );

   ChartRedraw();

   Print(
      "TDI Dashboard: JSON read successfully | ",
      file_name,
      " | characters=",
      StringLen(content)
   );
}

//+------------------------------------------------------------------+
//| Custom indicator iteration                                       |
//+------------------------------------------------------------------+
int OnCalculate(
   const int rates_total,
   const int prev_calculated,
   const datetime &time[],
   const double &open[],
   const double &high[],
   const double &low[],
   const double &close[],
   const long &tick_volume[],
   const long &volume[],
   const int &spread[]
)
{
   return(rates_total);
}
