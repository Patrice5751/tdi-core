#property copyright "TDI"
#property version   "1.00"
#property indicator_chart_window
#property indicator_plots 0
#include <Canvas\Canvas.mqh>

CCanvas g_bias_canvas;

int g_panel_x = 10;
int g_panel_y = 10;

input int RefreshSeconds = 2;
input int StaleAfterSeconds = 90;

void CreateGaugeSegment(
   string name,
   int x,
   int y,
   color segment_color
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
      OBJPROP_XDISTANCE, x
   );

   ObjectSetInteger(
      0, name,
      OBJPROP_YDISTANCE, y
   );

   ObjectSetInteger(
      0, name,
      OBJPROP_XSIZE, 10
   );

   ObjectSetInteger(
      0, name,
      OBJPROP_YSIZE, 4
   );

   ObjectSetInteger(
      0, name,
      OBJPROP_BGCOLOR, segment_color
   );

   ObjectSetInteger(
      0, name,
      OBJPROP_BORDER_COLOR, segment_color
   );
}
void UpdateBiasGauge(int score)
{
   int active_segments = (score * 11 + 99) / 100;

   if(active_segments < 0)
      active_segments = 0;

   if(active_segments > 11)
      active_segments = 11;

   for(int i = 0; i < 11; i++)
   {
      string name = StringFormat(
         "TDI_BIAS_GAUGE_%02d",
         i
      );

      color segment_color =
         (i < active_segments)
         ? clrYellow
         : clrDimGray;

      ObjectSetInteger(
         0,
         name,
         OBJPROP_BGCOLOR,
         segment_color
      );

      ObjectSetInteger(
         0,
         name,
         OBJPROP_BORDER_COLOR,
         segment_color
      );
   }
}

void UpdateScenarioGauge(int score)
{
   int active_segments = (score * 11 + 99) / 100;

   if(active_segments < 0)
      active_segments = 0;

   if(active_segments > 11)
      active_segments = 11;

   for(int i = 0; i < 11; i++)
   {
      string name = StringFormat(
         "TDI_SCENARIO_GAUGE_%02d",
         i
      );

      color segment_color =
         (i < active_segments)
         ? clrDodgerBlue
         : clrDimGray;

      ObjectSetInteger(
         0,
         name,
         OBJPROP_BGCOLOR,
         segment_color
      );

      ObjectSetInteger(
         0,
         name,
         OBJPROP_BORDER_COLOR,
         segment_color
      );
   }
}
//+------------------------------------------------------------------+
//| Custom indicator initialization                                  |
//+------------------------------------------------------------------+
void UpdateBiasSmoothGauge(int score)
{
   if(score < 0)
      score = 0;

   if(score > 100)
      score = 100;

   double pi = 3.14159265358979323846;
   double active_angle = pi * score / 100.0;

   g_bias_canvas.Erase(clrBlack);

   // Fond gris plus epais
   for(int t = 0; t < 6; t++)
   {
      g_bias_canvas.Arc(
         60,
         60,
         60 - t,
         50 - t,
         0.0,
         pi,
         clrDimGray
      );
   }

   // Partie active
   if(score > 0)
   {
      color gauge_color = clrDodgerBlue;

      if(score >= 90)
         gauge_color = clrLimeGreen;
      else if(score >= 80)
         gauge_color = clrGreenYellow;
      else if(score >= 70)
         gauge_color = clrYellow;
      else if(score >= 60)
         gauge_color = clrOrange;

      double start_angle = pi - active_angle;

      for(int t = 0; t < 6; t++)
      {
         g_bias_canvas.Arc(
            60,
            60,
            60 - t,
            50 - t,
            start_angle,
            pi,
            gauge_color
         );
      }
   }

   g_bias_canvas.FontSet("Arial", 18);

   g_bias_canvas.TextOut(
      40,
      45,
      IntegerToString(score) + "/100",
      White
   );

   g_bias_canvas.Update();
}

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
      850
   );

   ObjectSetInteger(
      0,
      panel_name,
      OBJPROP_BGCOLOR,
      C'8,12,20'
   );

   ObjectSetInteger(
      0,
      panel_name,
      OBJPROP_COLOR,
      clrSilver
   );

   ObjectSetInteger(
      0,
      panel_name,
      OBJPROP_STYLE,
      STYLE_SOLID
   );

   ObjectSetInteger(
      0,
      panel_name,
      OBJPROP_BORDER_TYPE,
      BORDER_FLAT
   );

   ObjectSetInteger(
      0,
      panel_name,
      OBJPROP_WIDTH,
      1
   );

   ObjectSetInteger(
      0,
      panel_name,
      OBJPROP_SELECTABLE,
      true
   );

   ObjectSetInteger(
      0,
      panel_name,
      OBJPROP_SELECTED,
      true
   );

   ObjectSetInteger(
      0,
      panel_name,
      OBJPROP_ZORDER,
      100
   );

   CreateGaugeSegment("TDI_BIAS_GAUGE_00", 125, 295, clrYellow);
   CreateGaugeSegment("TDI_BIAS_GAUGE_01", 129, 280, clrYellow);
   CreateGaugeSegment("TDI_BIAS_GAUGE_02", 139, 267, clrYellow);
   CreateGaugeSegment("TDI_BIAS_GAUGE_03", 153, 257, clrYellow);
   CreateGaugeSegment("TDI_BIAS_GAUGE_04", 169, 251, clrYellow);
   CreateGaugeSegment("TDI_BIAS_GAUGE_05", 185, 249, clrYellow);
   CreateGaugeSegment("TDI_BIAS_GAUGE_06", 201, 251, clrYellow);
   CreateGaugeSegment("TDI_BIAS_GAUGE_07", 217, 257, clrYellow);
   CreateGaugeSegment("TDI_BIAS_GAUGE_08", 231, 267, clrYellow);
   CreateGaugeSegment("TDI_BIAS_GAUGE_09", 241, 280, clrYellow);
   CreateGaugeSegment("TDI_BIAS_GAUGE_10", 245, 295, clrDimGray);

   string bias_gauge_value_name = "TDI_BIAS_GAUGE_VALUE";

   ObjectCreate(
      0,
      bias_gauge_value_name,
      OBJ_LABEL,
      0,
      0,
      0
   );

   ObjectSetInteger(
      0,
      bias_gauge_value_name,
      OBJPROP_CORNER,
      CORNER_LEFT_UPPER
   );

   ObjectSetInteger(
      0,
      bias_gauge_value_name,
      OBJPROP_XDISTANCE,
      185
   );

   ObjectSetInteger(
      0,
      bias_gauge_value_name,
      OBJPROP_YDISTANCE,
      240
   );

   ObjectSetInteger(
      0,
      bias_gauge_value_name,
      OBJPROP_FONTSIZE,
      11
   );

   ObjectSetInteger(
      0,
      bias_gauge_value_name,
      OBJPROP_COLOR,
      clrYellow
   );

   ObjectSetString(
      0,
      bias_gauge_value_name,
      OBJPROP_TEXT,
      "0/100"
   );

   ObjectDelete(
      0,
      "TDI_BIAS_GAUGE_VALUE"
   );

    for(int i = 0; i <= 10; i++)
   {
      string name = StringFormat(
         "TDI_BIAS_GAUGE_%02d",
         i
      );

      if(ObjectFind(0, name) >= 0)
         ObjectDelete(0, name);
   }

   CreateGaugeSegment("TDI_SCENARIO_GAUGE_00", 125, 550, clrDodgerBlue);
   CreateGaugeSegment("TDI_SCENARIO_GAUGE_01", 129, 535, clrDodgerBlue);
   CreateGaugeSegment("TDI_SCENARIO_GAUGE_02", 139, 522, clrDodgerBlue);
   CreateGaugeSegment("TDI_SCENARIO_GAUGE_03", 153, 512, clrDodgerBlue);
   CreateGaugeSegment("TDI_SCENARIO_GAUGE_04", 169, 506, clrDodgerBlue);
   CreateGaugeSegment("TDI_SCENARIO_GAUGE_05", 185, 504, clrDodgerBlue);
   CreateGaugeSegment("TDI_SCENARIO_GAUGE_06", 201, 506, clrDodgerBlue);
   CreateGaugeSegment("TDI_SCENARIO_GAUGE_07", 217, 512, clrDodgerBlue);
   CreateGaugeSegment("TDI_SCENARIO_GAUGE_08", 231, 522, clrDodgerBlue);
   CreateGaugeSegment("TDI_SCENARIO_GAUGE_09", 241, 535, clrDodgerBlue);
   CreateGaugeSegment("TDI_SCENARIO_GAUGE_10", 245, 550, clrDodgerBlue);

   string scenario_gauge_value_name = "TDI_SCENARIO_GAUGE_VALUE";

   ObjectCreate(
      0,
      scenario_gauge_value_name,
      OBJ_LABEL,
      0,
      0,
      0
   );

   ObjectSetInteger(
      0,
      scenario_gauge_value_name,
      OBJPROP_CORNER,
      CORNER_LEFT_UPPER
   );

   ObjectSetInteger(
      0,
      scenario_gauge_value_name,
      OBJPROP_XDISTANCE,
      185
   );

   ObjectSetInteger(
      0,
      scenario_gauge_value_name,
      OBJPROP_YDISTANCE,
      530
   );

   ObjectSetInteger(
      0,
      scenario_gauge_value_name,
      OBJPROP_FONTSIZE,
      11
   );

   ObjectSetInteger(
      0,
      scenario_gauge_value_name,
      OBJPROP_COLOR,
      clrDodgerBlue
   );

   ObjectSetString(
      0,
      scenario_gauge_value_name,
      OBJPROP_TEXT,
      "0/100"
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
   string decision_value_name = "TDI_DECISION_VALUE";
   string preferred_name = "TDI_PREFERRED_SIDE";
   string preferred_value_name = "TDI_PREFERRED_SIDE_VALUE";
   string target_name = "TDI_TARGET_SIDE";
   string target_value_name = "TDI_TARGET_SIDE_VALUE";


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
   0, decision_value_name, OBJ_LABEL, 0, 0, 0
   );

   ObjectSetInteger(
      0, decision_value_name,
      OBJPROP_CORNER, CORNER_LEFT_UPPER
   );

   ObjectSetInteger(
      0, decision_value_name,
      OBJPROP_XDISTANCE, 205
   );

   ObjectSetInteger(
      0, decision_value_name,
      OBJPROP_YDISTANCE, 78
   );

   ObjectSetInteger(
      0, decision_value_name,
      OBJPROP_COLOR, clrYellow
   );

   ObjectSetInteger(
      0, decision_value_name,
      OBJPROP_FONTSIZE, 14
   );

   ObjectSetString(
      0, decision_value_name,
      OBJPROP_TEXT, "WAIT"
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
      OBJPROP_TEXT, "Preferred side : -"
   );
   ObjectCreate(
   0, preferred_value_name, OBJ_LABEL, 0, 0, 0
   );

   ObjectSetInteger(
      0, preferred_value_name,
      OBJPROP_CORNER, CORNER_LEFT_UPPER
   );

   ObjectSetInteger(
      0, preferred_value_name,
      OBJPROP_XDISTANCE, 205
   );

   ObjectSetInteger(
      0, preferred_value_name,
      OBJPROP_YDISTANCE, 105
   );

   ObjectSetInteger(
      0, preferred_value_name,
      OBJPROP_COLOR, clrSilver
   );

   ObjectSetInteger(
      0, preferred_value_name,
      OBJPROP_FONTSIZE, 10
   );

   ObjectSetString(
      0, preferred_value_name,
      OBJPROP_TEXT, "NONE"
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
      OBJPROP_TEXT, "Target side    : -"
   );
   ObjectCreate(
      0, target_value_name, OBJ_LABEL, 0, 0, 0
   );

   ObjectSetInteger(
      0, target_value_name,
      OBJPROP_CORNER, CORNER_LEFT_UPPER
   );

   ObjectSetInteger(
      0, target_value_name,
      OBJPROP_XDISTANCE, 205
   );

   ObjectSetInteger(
      0, target_value_name,
      OBJPROP_YDISTANCE, 130
   );

   ObjectSetInteger(
      0, target_value_name,
      OBJPROP_COLOR, clrSilver
   );

   ObjectSetInteger(
      0, target_value_name,
      OBJPROP_FONTSIZE, 10
   );

   ObjectSetString(
      0, target_value_name,
      OBJPROP_TEXT, "NONE"
   );
      string bias_title_name = "TDI_BIAS_TITLE";
   string convergence_name = "TDI_BIAS_CONVERGENCE";
   string convergence_value_name = "TDI_BIAS_CONVERGENCE_VALUE";
   string readiness_name = "TDI_BIAS_READINESS";
   string readiness_value_name = "TDI_BIAS_READINESS_VALUE";
   string score_name = "TDI_BIAS_SCORE";

   CreateSectionSeparator(
      "TDI_SEPARATOR_BIAS",
      155
   );
   CreateSectionSeparator(
      "TDI_SEPARATOR_CONFIRMATION",
      315
   );
    CreateSectionSeparator(
      "TDI_SEPARATOR_SCENARIO",
      455
   );

   CreateSectionSeparator(
      "TDI_SEPARATOR_WAITING_FOR",
      640
   );
   CreateSectionSeparator(
      "TDI_SEPARATOR_TRANSITION",
      730
   );
   CreateSectionSeparator(
      "TDI_SEPARATOR_ALERT",
      785
   );
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
      OBJPROP_TEXT, "Convergence : -"
   );
   ObjectCreate(
      0, convergence_value_name, OBJ_LABEL, 0, 0, 0
   );

   ObjectSetInteger(
      0, convergence_value_name,
      OBJPROP_CORNER, CORNER_LEFT_UPPER
   );

   ObjectSetInteger(
      0, convergence_value_name,
      OBJPROP_XDISTANCE, 205
   );

   ObjectSetInteger(
      0, convergence_value_name,
      OBJPROP_YDISTANCE, 195
   );

   ObjectSetInteger(
      0, convergence_value_name,
      OBJPROP_COLOR, clrSilver
   );

   ObjectSetInteger(
      0, convergence_value_name,
      OBJPROP_FONTSIZE, 10
   );

   ObjectSetString(
      0, convergence_value_name,
      OBJPROP_TEXT, "UNDEFINED"
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
      OBJPROP_YDISTANCE, 210
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
      OBJPROP_TEXT, "Readiness : -"
   );
   ObjectCreate(
      0, readiness_value_name, OBJ_LABEL, 0, 0, 0
   );

   ObjectSetInteger(
      0, readiness_value_name,
      OBJPROP_CORNER, CORNER_LEFT_UPPER
   );

   ObjectSetInteger(
      0, readiness_value_name,
      OBJPROP_XDISTANCE, 205
   );

   ObjectSetInteger(
      0, readiness_value_name,
      OBJPROP_YDISTANCE, 210
   );

   ObjectSetInteger(
      0, readiness_value_name,
      OBJPROP_COLOR, clrSilver
   );

   ObjectSetInteger(
      0, readiness_value_name,
      OBJPROP_FONTSIZE, 10
   );

   ObjectSetString(
      0, readiness_value_name,
      OBJPROP_TEXT, "LOW"
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
      OBJPROP_YDISTANCE, 225
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
      OBJPROP_TEXT, "Score"
   );

   string bias_score_value_name = "TDI_BIAS_SCORE_VALUE";

   ObjectCreate(
      0, bias_score_value_name, OBJ_LABEL, 0, 0, 0
   );

   ObjectSetInteger(
      0, bias_score_value_name,
      OBJPROP_CORNER, CORNER_LEFT_UPPER
   );

   ObjectSetInteger(
      0, bias_score_value_name,
      OBJPROP_XDISTANCE, 205
   );

   ObjectSetInteger(
      0, bias_score_value_name,
      OBJPROP_YDISTANCE, 225
   );

   ObjectSetInteger(
      0, bias_score_value_name,
      OBJPROP_COLOR, clrSilver
   );

   ObjectSetInteger(
      0, bias_score_value_name,
      OBJPROP_FONTSIZE, 10
   );

   ObjectSetString(
      0, bias_score_value_name,
      OBJPROP_TEXT, "-/100"
   );


   if(
      !g_bias_canvas.CreateBitmapLabel(
         0,
         0,
         "TDI_BIAS_CANVAS",
         105,
         240,
         120,
         70,
         COLOR_FORMAT_XRGB_NOALPHA
      )
   )
   g_bias_canvas.Erase(ColorToARGB(clrRed, 255));

   g_bias_canvas.Erase(clrBlack);

   UpdateBiasSmoothGauge(100);

   {
      Print("TDI Dashboard: unable to create bias canvas");
   }


   ObjectSetInteger(
      0,
      "TDI_BIAS_CANVAS",
      OBJPROP_BACK,
      false
   );

   ObjectSetInteger(
      0,
      "TDI_BIAS_CANVAS",
      OBJPROP_ZORDER,
      200
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
      OBJPROP_YDISTANCE, 470
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
      OBJPROP_YDISTANCE, 565
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
      OBJPROP_TEXT, "State"
   );

   string scenario_state_value_name = "TDI_SCENARIO_STATE_VALUE";

   ObjectCreate(
      0, scenario_state_value_name, OBJ_LABEL, 0, 0, 0
   );

   ObjectSetInteger(
      0, scenario_state_value_name,
      OBJPROP_CORNER, CORNER_LEFT_UPPER
   );

   ObjectSetInteger(
      0, scenario_state_value_name,
      OBJPROP_XDISTANCE, 205
   );

   ObjectSetInteger(
      0, scenario_state_value_name,
      OBJPROP_YDISTANCE, 565
   );

   ObjectSetInteger(
      0, scenario_state_value_name,
      OBJPROP_COLOR, clrSilver
   );

   ObjectSetInteger(
      0, scenario_state_value_name,
      OBJPROP_FONTSIZE, 10
   );

   ObjectSetString(
      0, scenario_state_value_name,
      OBJPROP_TEXT, "-"
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
      OBJPROP_YDISTANCE, 485
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
      OBJPROP_TEXT, "Score"
   );

   string scenario_score_value_name = "TDI_SCENARIO_SCORE_VALUE";

   ObjectCreate(
      0, scenario_score_value_name, OBJ_LABEL, 0, 0, 0
   );

   ObjectSetInteger(
      0, scenario_score_value_name,
      OBJPROP_CORNER, CORNER_LEFT_UPPER
   );

   ObjectSetInteger(
      0, scenario_score_value_name,
      OBJPROP_XDISTANCE, 205
   );

   ObjectSetInteger(
      0, scenario_score_value_name,
      OBJPROP_YDISTANCE, 485
   );

   ObjectSetInteger(
      0, scenario_score_value_name,
      OBJPROP_COLOR, clrSilver
   );

   ObjectSetInteger(
      0, scenario_score_value_name,
      OBJPROP_FONTSIZE, 10
   );

   ObjectSetString(
      0, scenario_score_value_name,
      OBJPROP_TEXT, "-/100"
   );

      string confirmation_title_name = "TDI_CONFIRMATION_TITLE";
   string bias_aligned_name = "TDI_CONFIRMATION_BIAS";
   string bias_aligned_value_name = "TDI_CONFIRMATION_BIAS_VALUE";
   string structure_aligned_name = "TDI_CONFIRMATION_STRUCTURE";
   string structure_aligned_value_name = "TDI_CONFIRMATION_STRUCTURE_VALUE";
   string timing_favorable_name = "TDI_CONFIRMATION_TIMING";
   string timing_favorable_value_name = "TDI_CONFIRMATION_TIMING_VALUE";
   string momentum_confirmed_name = "TDI_CONFIRMATION_MOMENTUM";
   string momentum_confirmed_value_name = "TDI_CONFIRMATION_MOMENTUM_VALUE";


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
      OBJPROP_YDISTANCE, 330
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
      OBJPROP_YDISTANCE, 355
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
      OBJPROP_TEXT, "Bias aligned      : -"
   );
   ObjectCreate(
      0, bias_aligned_value_name, OBJ_LABEL, 0, 0, 0
   );

   ObjectSetInteger(
      0, bias_aligned_value_name,
      OBJPROP_CORNER, CORNER_LEFT_UPPER
   );

   ObjectSetInteger(
      0, bias_aligned_value_name,
      OBJPROP_XDISTANCE, 205
   );

   ObjectSetInteger(
      0, bias_aligned_value_name,
      OBJPROP_YDISTANCE, 355
   );

   ObjectSetInteger(
      0, bias_aligned_value_name,
      OBJPROP_COLOR, clrTomato
   );

   ObjectSetInteger(
      0, bias_aligned_value_name,
      OBJPROP_FONTSIZE, 10
   );

   ObjectSetString(
      0, bias_aligned_value_name,
      OBJPROP_TEXT, "NO"
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
      OBJPROP_YDISTANCE, 380
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
      OBJPROP_TEXT, "Structure aligned : -"
   );
   ObjectCreate(
      0, structure_aligned_value_name, OBJ_LABEL, 0, 0, 0
   );

   ObjectSetInteger(
      0, structure_aligned_value_name,
      OBJPROP_CORNER, CORNER_LEFT_UPPER
   );

   ObjectSetInteger(
      0, structure_aligned_value_name,
      OBJPROP_XDISTANCE, 205
   );

   ObjectSetInteger(
      0, structure_aligned_value_name,
      OBJPROP_YDISTANCE, 380
   );

   ObjectSetInteger(
      0, structure_aligned_value_name,
      OBJPROP_COLOR, clrSilver
   );

   ObjectSetInteger(
      0, structure_aligned_value_name,
      OBJPROP_FONTSIZE, 10
   );

   ObjectSetString(
      0, structure_aligned_value_name,
      OBJPROP_TEXT, "NO"
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
      OBJPROP_YDISTANCE, 405
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
      OBJPROP_TEXT, "Timing favorable  : -"
   );
   ObjectCreate(
      0, timing_favorable_value_name, OBJ_LABEL, 0, 0, 0
   );

   ObjectSetInteger(
      0, timing_favorable_value_name,
      OBJPROP_CORNER, CORNER_LEFT_UPPER
   );

   ObjectSetInteger(
      0, timing_favorable_value_name,
      OBJPROP_XDISTANCE, 205
   );

   ObjectSetInteger(
      0, timing_favorable_value_name,
      OBJPROP_YDISTANCE, 405
   );

   ObjectSetInteger(
      0, timing_favorable_value_name,
      OBJPROP_COLOR, clrSilver
   );

   ObjectSetInteger(
      0, timing_favorable_value_name,
      OBJPROP_FONTSIZE, 10
   );

   ObjectSetString(
      0, timing_favorable_value_name,
      OBJPROP_TEXT, "NO"
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
      OBJPROP_YDISTANCE, 430
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
      OBJPROP_TEXT, "Momentum confirmed: -"
   );
   ObjectCreate(
      0, momentum_confirmed_value_name, OBJ_LABEL, 0, 0, 0
   );

   ObjectSetInteger(
      0, momentum_confirmed_value_name,
      OBJPROP_CORNER, CORNER_LEFT_UPPER
   );

   ObjectSetInteger(
      0, momentum_confirmed_value_name,
      OBJPROP_XDISTANCE, 205
   );

   ObjectSetInteger(
      0, momentum_confirmed_value_name,
      OBJPROP_YDISTANCE, 430
   );

   ObjectSetInteger(
      0, momentum_confirmed_value_name,
      OBJPROP_COLOR, clrSilver
   );

   ObjectSetInteger(
      0, momentum_confirmed_value_name,
      OBJPROP_FONTSIZE, 10
   );

   ObjectSetString(
      0, momentum_confirmed_value_name,
      OBJPROP_TEXT, "NO"
   );


   string global_score_title_name = "TDI_GLOBAL_SCORE_TITLE";
   string global_score_value_name = "TDI_GLOBAL_SCORE_VALUE";
   string global_grade_name = "TDI_GLOBAL_GRADE";

   CreateSectionSeparator(
      "TDI_SEPARATOR_GLOBAL_SCORE",
      590
   );
   ObjectCreate(
      0, global_score_title_name, OBJ_LABEL, 0, 0, 0
   );
   ObjectSetInteger(
      0, global_score_title_name,
      OBJPROP_CORNER, CORNER_LEFT_UPPER
   );
   ObjectSetInteger(
      0, global_score_title_name,
      OBJPROP_XDISTANCE, 25
   );
   ObjectSetInteger(
      0, global_score_title_name,
      OBJPROP_YDISTANCE, 600
   );
   ObjectSetInteger(
      0, global_score_title_name,
      OBJPROP_COLOR, clrWhite
   );
   ObjectSetInteger(
      0, global_score_title_name,
      OBJPROP_FONTSIZE, 11
   );
   ObjectSetString(
      0, global_score_title_name,
      OBJPROP_TEXT, "GLOBAL SCORE"
   );

   ObjectCreate(
      0, global_score_value_name, OBJ_LABEL, 0, 0, 0
   );
   ObjectSetInteger(
      0, global_score_value_name,
      OBJPROP_CORNER, CORNER_LEFT_UPPER
   );
   ObjectSetInteger(
      0, global_score_value_name,
      OBJPROP_XDISTANCE, 205
   );
   ObjectSetInteger(
      0, global_score_value_name,
      OBJPROP_YDISTANCE, 600
   );
   ObjectSetInteger(
      0, global_score_value_name,
      OBJPROP_COLOR, clrSilver
   );
   ObjectSetInteger(
      0, global_score_value_name,
      OBJPROP_FONTSIZE, 10
   );
   ObjectSetString(
      0, global_score_value_name,
      OBJPROP_TEXT, "-/100"
   );

   ObjectCreate(
      0, global_grade_name, OBJ_LABEL, 0, 0, 0
   );
   ObjectSetInteger(
      0, global_grade_name,
      OBJPROP_CORNER, CORNER_LEFT_UPPER
   );
   ObjectSetInteger(
      0, global_grade_name,
      OBJPROP_XDISTANCE, 25
   );
   ObjectSetInteger(
      0, global_grade_name,
      OBJPROP_YDISTANCE, 620
   );
   ObjectSetInteger(
      0, global_grade_name,
      OBJPROP_COLOR, clrSilver
   );
   ObjectSetInteger(
      0, global_grade_name,
      OBJPROP_FONTSIZE, 10
   );
   ObjectSetString(
      0, global_grade_name,
      OBJPROP_TEXT, "Grade : -"
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
      OBJPROP_YDISTANCE, 650
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
      OBJPROP_YDISTANCE, 672
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
      OBJPROP_YDISTANCE, 690
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
      "-"
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
      OBJPROP_YDISTANCE, 708
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
      "-"
   );
   ObjectSetString(
      0, waiting_value_name,
      OBJPROP_TEXT, "-"
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
      OBJPROP_YDISTANCE, 745
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
      OBJPROP_YDISTANCE, 765
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
      OBJPROP_TEXT, "-"
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
      OBJPROP_YDISTANCE, 785
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
      OBJPROP_YDISTANCE, 807
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
      OBJPROP_TEXT, "Level : -"
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
      OBJPROP_XDISTANCE, 155
   );
   ObjectSetInteger(
      0, alert_active_name,
      OBJPROP_YDISTANCE, 807
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
      OBJPROP_TEXT, "Active : -"
   );

   CreateSectionSeparator(
      "TDI_SEPARATOR_INTERMARKET",
      827
   );

   string intermarket_name =
      "TDI_INTERMARKET";

   ObjectCreate(
      0,
      intermarket_name,
      OBJ_LABEL,
      0,
      0,
      0
   );

   ObjectSetInteger(
      0,
      intermarket_name,
      OBJPROP_CORNER,
      CORNER_LEFT_UPPER
   );

   ObjectSetInteger(
      0,
      intermarket_name,
      OBJPROP_XDISTANCE,
      25
   );

   ObjectSetInteger(
      0,
      intermarket_name,
      OBJPROP_YDISTANCE,
      837
   );

   ObjectSetInteger(
      0,
      intermarket_name,
      OBJPROP_COLOR,
      clrSilver
   );

   ObjectSetInteger(
      0,
      intermarket_name,
      OBJPROP_FONTSIZE,
      10
   );

   ObjectSetString(
      0,
      intermarket_name,
      OBJPROP_TEXT,
      "INTERMARKET   -   -/100"
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
      return("-");

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
      return("-");

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
      return("-");

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

   return("-");
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

void UpdateIntermarketDisplay()
{
   string object_name = "TDI_INTERMARKET";

   ObjectSetString(
      0,
      object_name,
      OBJPROP_TEXT,
      "INTERMARKET   -   -/100"
   );

   ObjectSetInteger(
      0,
      object_name,
      OBJPROP_COLOR,
      clrSilver
   );

   string file_name =
      "intermarket_XAUUSD_XAGUSD.json";

   int handle = FileOpen(
      file_name,
      FILE_READ | FILE_TXT | FILE_ANSI
   );

   if(handle == INVALID_HANDLE)
      return;

   string content = "";

   while(!FileIsEnding(handle))
   {
      content += FileReadString(handle);
   }

   FileClose(handle);

   string state = JsonGetString(
      content,
      "state"
   );

   int score = JsonGetInt(
      content,
      "score"
   );

   if(state == "")
      return;

   string state_upper = state;
   StringToUpper(state_upper);

   ObjectSetString(
      0,
      object_name,
      OBJPROP_TEXT,
      "INTERMARKET   "
      + state_upper
      + "   "
      + IntegerToString(score)
      + "/100"
   );

   color state_color = clrSilver;

   if(state_upper == "CONFIRMED")
      state_color = clrLimeGreen;
   else if(state_upper == "MIXED")
      state_color = clrYellow;
   else if(state_upper == "DIVERGENT")
      state_color = clrTomato;

   ObjectSetInteger(
      0,
      object_name,
      OBJPROP_COLOR,
      state_color
   );
}

void OnTimer()

{
   int current_x = (int)ObjectGetInteger(
      0,
      "TDI_PANEL_BACKGROUND",
      OBJPROP_XDISTANCE
   );

   int current_y = (int)ObjectGetInteger(
      0,
      "TDI_PANEL_BACKGROUND",
      OBJPROP_YDISTANCE
   );

   int dx = current_x - g_panel_x;
   int dy = current_y - g_panel_y;

   if(dx != 0 || dy != 0)
   {
      int total_objects = ObjectsTotal(0, -1, -1);

      for(int i = 0; i < total_objects; i++)
      {
         string object_name = ObjectName(0, i, -1, -1);

         if(
            StringFind(object_name, "TDI_") == 0 &&
            object_name != "TDI_PANEL_BACKGROUND"
         )
         {
            int object_x = (int)ObjectGetInteger(
               0,
               object_name,
               OBJPROP_XDISTANCE
            );

            int object_y = (int)ObjectGetInteger(
               0,
               object_name,
               OBJPROP_YDISTANCE
            );

            ObjectSetInteger(
               0,
               object_name,
               OBJPROP_XDISTANCE,
               object_x + dx
            );

            ObjectSetInteger(
               0,
               object_name,
               OBJPROP_YDISTANCE,
               object_y + dy
            );
         }
      }

      g_panel_x = current_x;
      g_panel_y = current_y;

      ChartRedraw();
   }

   UpdateIntermarketDisplay();

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

   string opportunity = JsonGetString(
      content,
      "opportunity"
   );

   string h4_momentum = JsonGetString(
      content,
      "h4_momentum"
   );

   int h4_momentum_confidence = JsonGetInt(
      content,
      "h4_momentum_confidence"
   );

   string h1_momentum = JsonGetString(
      content,
      "h1_momentum"
   );

   int h1_momentum_confidence = JsonGetInt(
      content,
      "h1_momentum_confidence"
   );

   string h4_momentum_short = "?";
   string h1_momentum_short = "?";

   if(h4_momentum == "Bullish")
      h4_momentum_short = "B";
   else if(h4_momentum == "Bearish")
      h4_momentum_short = "S";
   else if(h4_momentum == "Neutral")
      h4_momentum_short = "N";

   if(h1_momentum == "Bullish")
      h1_momentum_short = "B";
   else if(h1_momentum == "Bearish")
      h1_momentum_short = "S";
   else if(h1_momentum == "Neutral")
      h1_momentum_short = "N";

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

   UpdateBiasSmoothGauge(bias_score);

   int scenario_score = JsonGetInt(
      content,
      "scenario_score"
   );

      string waiting_for = JsonGetArrayStringAt(
         content,
         "waiting_for",
         0
      );
      int global_score = JsonGetInt(
         content,
         "global_score"
      );

      string global_grade = JsonGetString(
         content,
         "global_grade"
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
      + (opportunity != "" && opportunity != "None"
         ? opportunity
         : decision)
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
   string decision_display = decision;
   StringToUpper(decision_display);

   string preferred_side_display = preferred_side;
   StringToUpper(preferred_side_display);
   string target_side_display = target_side;
   StringToUpper(target_side_display);
   string bias_convergence_display = bias_convergence;
   StringToUpper(bias_convergence_display);
   string bias_readiness_display = bias_readiness;
   StringToUpper(bias_readiness_display);

   ObjectSetString(
      0,
      "TDI_DECISION_VALUE",
      OBJPROP_TEXT,
      decision_display
   );

   ObjectSetInteger(
      0,
      "TDI_DECISION_VALUE",
      OBJPROP_COLOR,
      decision == "Buy"
      ? clrLimeGreen
      : decision == "Sell"
      ? clrTomato
      : clrYellow
   );
      ObjectSetString(
      0,
      "TDI_PREFERRED_SIDE",
      OBJPROP_TEXT,
      "Preferred side"
   );
      ObjectSetString(
      0,
      "TDI_PREFERRED_SIDE_VALUE",
      OBJPROP_TEXT,
      preferred_side_display
   );
   ObjectSetString(
      0,
      "TDI_TARGET_SIDE",
      OBJPROP_TEXT,
      "Target side"
   );
   ObjectSetString(
      0,
      "TDI_TARGET_SIDE_VALUE",
      OBJPROP_TEXT,
      target_side_display
   );
      ObjectSetString(
      0,
      "TDI_BIAS_CONVERGENCE",
      OBJPROP_TEXT,
      "Convergence"
   );

   ObjectSetString(
      0,
      "TDI_BIAS_CONVERGENCE_VALUE",
      OBJPROP_TEXT,
      bias_convergence_display
   );
   ObjectSetInteger(
      0,
      "TDI_BIAS_CONVERGENCE_VALUE",
      OBJPROP_COLOR,
      bias_convergence == "Aligned"
      ? clrLimeGreen
      : bias_convergence == "Toward"
      ? clrYellow
      : bias_convergence == "Away"
      ? clrTomato
      : clrSilver
   );
   ObjectSetString(
      0,
      "TDI_BIAS_READINESS",
      OBJPROP_TEXT,
      "Readiness"
   );

   ObjectSetString(
      0,
      "TDI_BIAS_READINESS_VALUE",
      OBJPROP_TEXT,
      bias_readiness_display
   );
   ObjectSetInteger(
      0,
      "TDI_BIAS_READINESS_VALUE",
      OBJPROP_COLOR,
      bias_readiness == "High"
      ? clrLimeGreen
      : bias_readiness == "Medium"
      ? clrYellow
      : clrSilver
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
      "Score"
   );

   ObjectSetString(
      0,
      "TDI_BIAS_SCORE_VALUE",
      OBJPROP_TEXT,
      IntegerToString(bias_score) + "/100"
   );

   ObjectSetInteger(
      0,
      "TDI_BIAS_SCORE",
      OBJPROP_ZORDER,
      300
   );

   ObjectSetInteger(
      0,
      "TDI_BIAS_SCORE_VALUE",
      OBJPROP_ZORDER,
      300
   );

   UpdateBiasGauge(bias_score);

   ObjectSetString(
      0,
      "TDI_BIAS_GAUGE_VALUE",
      OBJPROP_TEXT,
      IntegerToString(bias_score) + "/100"
   );

   ObjectSetInteger(
      0,
      "TDI_BIAS_GAUGE_VALUE",
      OBJPROP_ZORDER,
      300
   );

   ObjectSetString(
      0,
      "TDI_CONFIRMATION_BIAS",
      OBJPROP_TEXT,
      "Bias aligned"
   );

   ObjectSetInteger(
      0,
      "TDI_CONFIRMATION_BIAS",
      OBJPROP_COLOR,
      clrSilver
   );

   ObjectSetString(
      0,
      "TDI_CONFIRMATION_BIAS_VALUE",
      OBJPROP_TEXT,
      bias_aligned == "True"
      ? "YES"
      : "NO"
   );

   ObjectSetInteger(
      0,
      "TDI_CONFIRMATION_BIAS_VALUE",
      OBJPROP_COLOR,
      bias_aligned == "True"
      ? clrLimeGreen
      : clrTomato
   );

   ObjectSetString(
      0,
      "TDI_CONFIRMATION_STRUCTURE",
      OBJPROP_TEXT,
      "Structure aligned"
   );

   ObjectSetInteger(
      0,
      "TDI_CONFIRMATION_STRUCTURE",
      OBJPROP_COLOR,
      clrSilver
   );

   ObjectSetString(
      0,
      "TDI_CONFIRMATION_STRUCTURE_VALUE",
      OBJPROP_TEXT,
      structure_aligned == "True"
      ? "YES"
      : "NO"
   );

   ObjectSetInteger(
      0,
      "TDI_CONFIRMATION_STRUCTURE_VALUE",
      OBJPROP_COLOR,
      structure_aligned == "True"
      ? clrLimeGreen
      : clrTomato
   );

   ObjectSetString(
      0,
      "TDI_CONFIRMATION_TIMING",
      OBJPROP_TEXT,
      "Timing favorable"
   );

   ObjectSetInteger(
      0,
      "TDI_CONFIRMATION_TIMING",
      OBJPROP_COLOR,
      clrSilver
   );

   ObjectSetString(
      0,
      "TDI_CONFIRMATION_TIMING_VALUE",
      OBJPROP_TEXT,
      timing_favorable == "True"
      ? "YES"
      : "NO"
   );

   ObjectSetInteger(
      0,
      "TDI_CONFIRMATION_TIMING_VALUE",
      OBJPROP_COLOR,
      timing_favorable == "True"
      ? clrLimeGreen
      : clrTomato
   );

   ObjectSetString(
      0,
      "TDI_CONFIRMATION_MOMENTUM",
      OBJPROP_TEXT,
      "Momentum H4 / H1"
   );

   ObjectSetInteger(
      0,
      "TDI_CONFIRMATION_MOMENTUM",
      OBJPROP_COLOR,
      clrSilver
   );

   ObjectSetString(
      0,
      "TDI_CONFIRMATION_MOMENTUM_VALUE",
      OBJPROP_TEXT,
      h4_momentum_short
      + IntegerToString(h4_momentum_confidence)
      + " / "
      + h1_momentum_short
      + IntegerToString(h1_momentum_confidence)
   );

   ObjectSetInteger(
      0,
      "TDI_CONFIRMATION_MOMENTUM_VALUE",
      OBJPROP_COLOR,
      momentum_confirmed == "True"
      ? clrLimeGreen
      : clrTomato
   );

   ObjectSetString(
      0,
      "TDI_SCENARIO_STATE",
      OBJPROP_TEXT,
      "State"
   );

   ObjectSetString(
      0,
      "TDI_SCENARIO_STATE_VALUE",
      OBJPROP_TEXT,
      scenario_state
   );

   ObjectSetString(
      0,
      "TDI_GLOBAL_SCORE_VALUE",
      OBJPROP_TEXT,
      IntegerToString(global_score) + "/100"
   );

   ObjectSetString(
      0,
      "TDI_GLOBAL_GRADE",
      OBJPROP_TEXT,
      "Grade : " + global_grade
   );

   color global_score_color = clrTomato;

   if(global_score >= 90)
      global_score_color = clrLimeGreen;
   else if(global_score >= 80)
      global_score_color = clrGreenYellow;
   else if(global_score >= 70)
      global_score_color = clrYellow;
   else if(global_score >= 60)
      global_score_color = clrOrange;

   ObjectSetInteger(
      0,
      "TDI_GLOBAL_SCORE_VALUE",
      OBJPROP_COLOR,
      global_score_color
   );

   ObjectSetInteger(
      0,
      "TDI_GLOBAL_GRADE",
      OBJPROP_COLOR,
      global_score_color
   );

   ObjectSetInteger(
      0,
      "TDI_SCENARIO_STATE_VALUE",
      OBJPROP_COLOR,
      StringFind(scenario_state, "Ready") >= 0
      ? clrLimeGreen
      : StringFind(scenario_state, "Building") >= 0
        ? clrOrange
        : StringFind(scenario_state, "Degrading") >= 0
          ? clrOrangeRed
          : clrSilver
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
      "Score"
   );

   ObjectSetString(
      0,
      "TDI_SCENARIO_SCORE_VALUE",
      OBJPROP_TEXT,
      IntegerToString(scenario_score) + "/100"
   );

      UpdateScenarioGauge(scenario_score);

   ObjectSetString(
      0,
      "TDI_SCENARIO_GAUGE_VALUE",
      OBJPROP_TEXT,
      IntegerToString(scenario_score) + "/100"
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
