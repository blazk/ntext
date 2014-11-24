#!/usr/bin/env python


from ntext import Templates, trim
from util import Date


templ = Templates(

    st100 = '<task, param=stl,  num_layers=three_layers>',
    sm100 = '<task, param=swvl, num_layers=three_layers>',
    st20  = '<task, param=stl,  num_layers=two_layers>',
    sm20  = '<task, param=swvl, num_layers=two_layers>',

    task = trim(
        """

        export WDIR=%SMSWORK%
        export PARAM=%PARAM%
        export SCALE=%SCALE%
        export LSM=%LSM%

        mkdir $WDIR | true

        #Step 1 retrieve instantaneous fields

        export MARS_COMPUTE_FLAGS = 0

        (( FCLENGTH24=%FCLENGTH%-24 ))
        (( FCLENGTH18=%FCLENGTH%-18 ))
        (( FCLENGTH12=%FCLENGTH%-12 ))
        (( FCLENGTH6=%FCLENGTH%-6 ))

        mars \<\< EOF
        <retrieve_input, type=cf>
        <retrieve_input, type=pf>
        EOF

        <include_bitmaps>

        PARAM=%PARAM%

        mars \<\< EOF
        <compute, type=cf>
        <compute, type=pf>
        EOF

        mv ${PARAM}.cf $WDIR/${PARAM}.<ymd>.cf
        mv ${PARAM}.pf $WDIR/${PARAM}.<ymd>.pf

        """),


    retrieve_input = '<retrieve_input_<num_layers>>',


    retrieve_input_two_layers = trim(
        """

        RETRIEVE,
          param = <param>1,
          <member_selection_<type>>,
          class = od,
          levtype = sfc,
          expver = %EXPRT%,
          <stream>,
          date = <ymd>,
          time = 00,
          step = 0/to/$FCLENGTH6/BY/6,
          target = <param>1.input.<type>
        RETRIEVE,
          param = <param>2,
          target = <param>2.input.<type>
        """),


    retrieve_input_three_layers = trim(
        """
        <retrieve_input_two_layers>
        RETRIEVE,
          param = <param>3,
          target = <param>3.input.<type>
        """),


    compute = trim(
        """
        <retrieve_fieldset, fieldset_id=1>
        <retrieve_fieldset, fieldset_id=2>
        <retrieve_fieldset, fieldset_id=3>
        <retrieve_fieldset, fieldset_id=4>
        COMPUTE,
          fieldset=tn,
          accuracy=av,
          formula="<formula>"
        WRITE,
          fieldset=tn,
          target="${PARAM}.<type>"
        """),


    retrieve_fieldset = '<retrieve_fieldset_<num_layers>>',


    retrieve_fieldset_two_layers = trim(
        """
        <retrieve_fieldset_layer, layer_id=1>
        <retrieve_fieldset_layer, layer_id=2>
        """),


    retrieve_fieldset_three_layers = trim(
        """
        <retrieve_fieldset_two_layers>
        <retrieve_fieldset_layer, layer_id=3>
        """),


    retrieve_fieldset_layer = '<retrieve_fieldset_layer_<layer_id>>',


    retrieve_fieldset_layer_1 = trim(
        """

        RETRIEVE,
          source="<param><layer_id>.input.<type>",
          param=<param><layer_id>,
          type=<type>,
          class=od,
          levtype=sfc,
          expver=%EXPRT%,
          <stream>,
          date=<ymd>,
          time=00,
          <step_seq_for_fieldset_<fieldset_id>>,
          repres=LL,
          grid=1.5/1.5,
          fieldset=<layer_<layer_id>_symb><fieldset_id>
        """),


    retrieve_fieldset_layer_2 = trim(
        """
        RETRIEVE,
          source = "<param><layer_id>.input.<type>",
          param = <param><layer_id>,
          fieldset=<layer_<layer_id>_symb><fieldset_id>
        """),


    retrieve_fieldset_layer_3 = '<retrieve_fieldset_layer_2>',


    stream = '<stream_<fam>>',


    stream_enfo = trim(
        """
        stream = enfo
        """
        ),

    stream_enfh = trim(
        """
        stream = enfh,
        hdate = <hdate>
        """
        ),

    stream_rt = '<stream_enfo>',

    stream_hc = '<stream_enfh>',

    member_selection_cf = 'type = cf',

    member_selection_pf = trim(
        """
        type = pf,
        number = 1/to/50'
        """),


    include_bitmaps = trim(
        """
        for PARAM in <param_list>; do
        FCLENGTH=$FCLENGTH6
        STEP=6
        %include \<bitmap.rt.h\>
        done
        """),

    param_list = '<param_list_<num_layers>>',
    param_list_two_layers = '<param>1 <param>2',
    param_list_three_layers = '<param_list_two_layers> <param>3',


    formula = '<formula_for_<num_layers>>',
    formula_for_three_layers = "((t1+t2+t3+t4)*7+21*(u1+u2+u3+u4)+72*(v1+v2+v3+v4)) <<param>_scale> / (4. * 100.)",
    formula_for_two_layers = "((t1+t2+t3+t4)*7+13*(u1+u2+u3+u4)) <<param>_scale> /(4. * 20)",

    swvl_scale = '* 1000.',
    stl_scale = '',

    step_seq_for_fieldset_1 = 'step = 0/to/$FCLENGTH24/by/24',
    step_seq_for_fieldset_2 = 'step = 6/to/$FCLENGTH18/by/24',
    step_seq_for_fieldset_3 = 'step = 12/to/$FCLENGTH12/by/24',
    step_seq_for_fieldset_4 = 'step = 18/to/$FCLENGTH6/by/24',

    layer_1_symb = 't',
    layer_2_symb = 'u',
    layer_3_symb = 'v',
)


# --------------------------------------------
# test
# --------------------------------------------


date = Date(year=2014, month=8, day=3)
fam = 'enfo'
hdate = '/'.join(['%02d' % y + date.m + date.d for y in xrange(20, 0, -1)])

templ.update(fam=fam, ymd=date.ymd, hdate=hdate)

print templ.expand('<st100>')
#print templ.expand('<sm100>')
#print templ.expand('<st20>')
#print templ.expand('<sm20>')
