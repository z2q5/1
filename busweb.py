# ===== استكمال الدوال المتبقية =====

def show_driver_page():
    """صفحة السائق"""
    if not st.session_state.driver_logged_in:
        # واجهة تسجيل الدخول
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 2rem;
                border-radius: 15px;
                margin-bottom: 2rem;
            '>
                <h2>🚌 {t('driver_title')}</h2>
                <p>سجل الدخول لعرض قائمة الطلاب ومتابعة الحضور</p>
            </div>
            """, unsafe_allow_html=True)
            
            bus_number = st.selectbox(
                f"**{t('select_bus')}**",
                ["1", "2", "3"],
                key="driver_bus_select"
            )
            
            password = st.text_input(
                f"**{t('password')}**",
                type="password",
                placeholder=t('password_placeholder'),
                key="driver_password"
            )
            
            if st.button(f"**🚀 {t('login')}**", use_container_width=True, key="driver_login_btn"):
                if password == st.session_state.bus_passwords.get(bus_number, ""):
                    st.session_state.driver_logged_in = True
                    st.session_state.current_bus = bus_number
                    st.success(t("login_success"))
                    st.rerun()
                else:
                    st.error(t("login_error"))
        
        with col2:
            st.markdown("""
            <div style='
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                color: white;
                padding: 2rem;
                border-radius: 15px;
                text-align: center;
                height: 300px;
                display: flex;
                flex-direction: column;
                justify-content: center;
            '>
                <h1>🚍</h1>
                <h3>نظام متابعة الباص</h3>
                <p>ادخل بيانات الدخول للوصول إلى لوحة التحكم</p>
            </div>
            """, unsafe_allow_html=True)
    
    else:
        # لوحة التحكم بعد تسجيل الدخول
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 1.5rem;
                border-radius: 15px;
                margin-bottom: 1rem;
            '>
                <h2>🚌 باص رقم {st.session_state.current_bus}</h2>
                <p>لوحة متابعة الطلاب والحضور</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if st.button(f"**🔄 تحديث البيانات**", use_container_width=True, key="refresh_driver"):
                st.rerun()
        
        with col3:
            if st.button(f"**🚪 {t('logout')}**", use_container_width=True, key="driver_logout"):
                st.session_state.driver_logged_in = False
                st.rerun()
        
        # إحصائيات سريعة
        bus_students = get_bus_students(st.session_state.current_bus)
        today_attendance = get_today_attendance_for_bus(st.session_state.current_bus)
        
        coming_count = len(today_attendance[today_attendance["status"] == "قادم"]) if not today_attendance.empty else 0
        total_count = len(bus_students)
        percentage = (coming_count / total_count * 100) if total_count > 0 else 0
        
        col_stat1, col_stat2, col_stat3 = st.columns(3)
        
        with col_stat1:
            st.markdown(f"""
            <div class="metric-card">
                <h4>👥 {t('total_students')}</h4>
                <h2 style="color: #667eea;">{total_count}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col_stat2:
            st.markdown(f"""
            <div class="metric-card">
                <h4>✅ {t('confirmed_attendance')}</h4>
                <h2 style="color: #10b981;">{coming_count}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col_stat3:
            st.markdown(f"""
            <div class="metric-card">
                <h4>📈 {t('attendance_percentage')}</h4>
                <h2 style="color: #f59e0b;">{percentage:.1f}%</h2>
            </div>
            """, unsafe_allow_html=True)
        
        # قائمة الطلاب
        st.subheader(f"📋 {t('coming_students')}")
        
        if not bus_students.empty:
            # دمج بيانات الحضور
            student_data = []
            for _, student in bus_students.iterrows():
                registered, status = has_student_registered_today(student["id"])
                student_status = status if registered else t("status_not_registered")
                status_color = "🟢" if student_status == "قادم" else "🔴" if student_status == "لن يحضر" else "⚪"
                
                student_data.append({
                    "الطالب": student["name"],
                    "الصف": student["grade"],
                    "الحالة": f"{status_color} {student_status}",
                    "رقم الوزارة": student["id"]
                })
            
            # عرض البيانات في جدول
            student_df = pd.DataFrame(student_data)
            st.dataframe(student_df, use_container_width=True, hide_index=True)
        else:
            st.info(f"**ℹ️ {t('no_students')}**")

def show_parents_page():
    """صفحة أولياء الأمور"""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        <div style='
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
        '>
            <h2>👨‍👩‍👧 {t('parents_title')}</h2>
            <p>تابع حالة ابنك ومعلومات الباص</p>
        </div>
        """, unsafe_allow_html=True)
        
        student_id = st.text_input(
            f"**🔍 {t('enter_student_id')}**",
            placeholder=t('parents_id_placeholder'),
            key="parent_student_id"
        )
        
        if student_id:
            student_info = st.session_state.students_df[
                st.session_state.students_df["id"].astype(str) == student_id.strip()
            ]
            
            if not student_info.empty:
                student = student_info.iloc[0]
                
                st.success(f"**🎓 تم العثور على الطالب: {student['name']}**")
                
                # معلومات الطالب
                col_info1, col_info2, col_info3 = st.columns(3)
                
                with col_info1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h4>📚 {t('grade')}</h4>
                        <h3>{student['grade']}</h3>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_info2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h4>🚍 {t('bus')}</h4>
                        <h3>{student['bus']}</h3>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_info3:
                    registered, status = has_student_registered_today(student_id)
                    status_text = status if registered else "لم يسجل بعد"
                    status_icon = "✅" if status == "قادم" else "❌" if status == "لن يحضر" else "⏳"
                    
                    st.markdown(f"""
                    <div class="metric-card">
                        <h4>📊 {t('today_status')}</h4>
                        <h3>{status_icon} {status_text}</h3>
                    </div>
                    """, unsafe_allow_html=True)
                
                if registered:
                    today_data = st.session_state.attendance_df[
                        (st.session_state.attendance_df["id"].astype(str) == student_id.strip()) &
                        (st.session_state.attendance_df["date"] == datetime.datetime.now().strftime("%Y-%m-%d"))
                    ]
                    
                    if not today_data.empty:
                        latest_record = today_data.iloc[-1]
                        st.info(f"**⏰ {t('registration_time')}: {latest_record['time']}**")
            
            else:
                st.error(f"**❌ {t('not_found')}**")
    
    with col2:
        st.markdown(f"""
        <div style='
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 15px;
            margin-bottom: 1rem;
            text-align: center;
        '>
            <h3>🚌 {t('bus_info')}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if student_id and not student_info.empty:
            student = student_info.iloc[0]
            bus_number = student["bus"]
            schedule = get_bus_schedule(bus_number)
            driver = get_driver_contact(bus_number)
            
            # جدول الباص
            st.markdown(f"""
            <div class="metric-card">
                <h4>⏰ {t('bus_schedule')}</h4>
                <p><strong>{t('morning_pickup')}:</strong> {schedule['morning']}</p>
                <p><strong>{t('evening_return')}:</strong> {schedule['evening']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # معلومات السائق
            st.markdown(f"""
            <div class="metric-card">
                <h4>📞 {t('driver_contact')}</h4>
                <p><strong>اسم السائق:</strong> {driver['name']}</p>
                <p><strong>رقم الهاتف:</strong> {driver['phone']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # موقع الباص
            st.markdown(f"""
            <div class="metric-card">
                <h4>📍 {t('bus_location')}</h4>
                <p><strong>{t('current_location')}:</strong> في الطريق إلى المدرسة</p>
                <div style="background: #e8f4fd; padding: 1rem; border-radius: 10px; margin-top: 0.5rem;">
                    <p style="margin: 0; color: #666; font-size: 0.9rem;">
                        🕒 آخر تحديث: {datetime.datetime.now().strftime("%H:%M")}
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)

def show_admin_page():
    """صفحة الإدارة"""
    if not st.session_state.admin_logged_in:
        # واجهة تسجيل الدخول
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 2rem;
                border-radius: 15px;
                margin-bottom: 2rem;
            '>
                <h2>🏫 {t('admin_title')}</h2>
                <p>سجل الدخول للإدارة المتقدمة للنظام</p>
            </div>
            """, unsafe_allow_html=True)
            
            password = st.text_input(
                f"**🔐 {t('admin_password')}**",
                type="password",
                placeholder="أدخل كلمة مرور الإدارة...",
                key="admin_password_input"
            )
            
            if st.button(f"**🚀 {t('login')}**", use_container_width=True, key="admin_login_btn"):
                if password == st.session_state.admin_password:
                    st.session_state.admin_logged_in = True
                    st.success(t("login_success"))
                    st.rerun()
                else:
                    st.error(t("login_error"))
        
        with col2:
            st.markdown("""
            <div style='
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                color: white;
                padding: 2rem;
                border-radius: 15px;
                text-align: center;
                height: 300px;
                display: flex;
                flex-direction: column;
                justify-content: center;
            '>
                <h1>🔒</h1>
                <h3>لوحة تحكم الإدارة</h3>
                <p>الدخول مخصص للمشرفين والمديرين فقط</p>
            </div>
            """, unsafe_allow_html=True)
    
    else:
        # لوحة تحكم الإدارة
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 1.5rem;
                border-radius: 15px;
                margin-bottom: 1rem;
            '>
                <h2>🏫 {t('admin_title')}</h2>
                <p>إدارة النظام والبيانات والإعدادات</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if st.button(f"**🔄 تحديث**", use_container_width=True, key="refresh_admin"):
                st.rerun()
        
        with col3:
            if st.button(f"**🚪 تسجيل الخروج**", use_container_width=True, key="admin_logout"):
                st.session_state.admin_logged_in = False
                st.rerun()
        
        # إحصائيات النظام
        st.subheader("📊 إحصائيات النظام")
        
        total_students = len(st.session_state.students_df)
        total_attendance = len(st.session_state.attendance_df)
        total_ratings = len(st.session_state.ratings_df)
        
        col_stat1, col_stat2, col_stat3 = st.columns(3)
        
        with col_stat1:
            st.markdown(f"""
            <div class="metric-card">
                <h4>👥 {t('students_count')}</h4>
                <h2 style="color: #667eea;">{total_students}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col_stat2:
            st.markdown(f"""
            <div class="metric-card">
                <h4>📝 {t('attendance_records')}</h4>
                <h2 style="color: #10b981;">{total_attendance}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col_stat3:
            avg_rating, rating_count = get_average_rating()
            st.markdown(f"""
            <div class="metric-card">
                <h4>⭐ التقييمات</h4>
                <h2 style="color: #f59e0b;">{rating_count}</h2>
                <p>متوسط: {avg_rating:.1f}/5</p>
            </div>
            """, unsafe_allow_html=True)
        
        # إدارة الطلاب
        st.subheader("👥 إدارة الطلاب")
        
        # عرض قائمة الطلاب
        if not st.session_state.students_df.empty:
            st.dataframe(st.session_state.students_df, use_container_width=True)
        else:
            st.info("لا يوجد طلاب مسجلين في النظام")
        
        # إجراءات النظام
        st.subheader("⚙️ إجراءات النظام")
        
        col_act1, col_act2, col_act3 = st.columns(3)
        
        with col_act1:
            if st.button("🔄 إعادة تعيين البيانات", use_container_width=True):
                initialize_data()
                st.success("تم إعادة تعيين البيانات بنجاح")
                st.rerun()
        
        with col_act2:
            if st.button("📥 نسخة احتياطية", use_container_width=True):
                save_data()
                st.success("تم إنشاء نسخة احتياطية بنجاح")
        
        with col_act3:
            if st.button("🔄 تحديث كلمات المرور", use_container_width=True):
                st.info("استخدم النموذج أدناه لتغيير كلمات المرور")

def show_support_page():
    """صفحة الدعم"""
    st.markdown(f"""
    <div style='
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
    '>
        <h2>🤖 {t('support_title')}</h2>
        <p>مركز المساعدة والدعم الفني - نحن هنا لمساعدتك</p>
    </div>
    """, unsafe_allow_html=True)
    
    # تبويبات الدعم
    tab1, tab2, tab3 = st.tabs(["💬 المساعد الذكي", "📧 التواصل مع المطور", "⭐ نظام التقييم"])
    
    with tab1:
        smart_ai_assistant()
    
    with tab2:
        contact_developer()
    
    with tab3:
        show_rating_system()

def show_about_page():
    """صفحة حول النظام"""
    st.markdown(f"""
    <div style='
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
    '>
        <h2>ℹ️ {t('about_title')}</h2>
        <p>{t('about_description')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # مميزات النظام
        st.subheader("🎯 المميزات الرئيسية")
        
        features = [
            ("🎓", t("feature1"), t("feature1_desc")),
            ("📍", t("feature2"), t("feature2_desc")),
            ("⭐", t("feature3"), t("feature3_desc")),
            ("🔔", t("feature4"), t("feature4_desc")),
            ("🎨", t("feature5"), t("feature5_desc")),
            ("🔒", t("feature6"), t("feature6_desc"))
        ]
        
        for icon, title, desc in features:
            with st.container():
                st.markdown(f"""
                <div class="feature-card">
                    <div style="display: flex; align-items: start; gap: 1rem;">
                        <div style="font-size: 2rem;">{icon}</div>
                        <div>
                            <h4 style="margin: 0 0 0.5rem 0;">{title}</h4>
                            <p style="margin: 0; opacity: 0.8;">{desc}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    with col2:
        # معلومات الفريق
        st.subheader("👥 فريق التطوير")
        
        team_members = [
            ("🛠️", t("developer"), "إياد مصطفى"),
            ("🎨", t("designer"), "ايمن جلال"),
            ("👨‍🏫", "المشرف", "قسم النادي البيئي")
        ]
        
        for icon, role, name in team_members:
            st.markdown(f"""
            <div class="metric-card">
                <div style="text-align: center;">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
                    <h4 style="margin: 0; color: #667eea;">{role}</h4>
                    <p style="margin: 0.5rem 0 0 0; font-weight: bold;">{name}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # معلومات الإصدار
        st.markdown(f"""
        <div class="metric-card">
            <h4>📋 {t('version_info')}</h4>
            <p><strong>{t('version')}:</strong> 2.0</p>
            <p><strong>{t('release_date')}:</strong> 2025</p>
            <p><strong>{t('status_stable')}</strong></p>
        </div>
        """, unsafe_allow_html=True)

def show_rating_system():
    """نظام التقييم"""
    st.subheader("⭐ نظام التقييم المتطور")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(f"""
        <div style='
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 15px;
            margin-bottom: 1rem;
            text-align: center;
        '>
            <h3>💬 {t('rate_app')}</h3>
            <p>شاركنا تجربتك مع النظام</p>
        </div>
        """, unsafe_allow_html=True)
        
        # اختيار التقييم
        rating = st.slider(
            f"**{t('your_rating')}**",
            1, 5, 5,
            key="rating_slider"
        )
        
        # عرض النجوم
        stars = "⭐" * rating + "☆" * (5 - rating)
        st.markdown(f"**{t('select_rating')}:** {stars}")
        
        # التعليق
        comment = st.text_area(
            f"**{t('your_comment')}**",
            placeholder="اكتب تعليقك هنا... (اختياري)",
            height=100,
            key="rating_comment"
        )
        
        if st.button(f"**🚀 {t('submit_rating')}**", use_container_width=True, key="submit_rating"):
            add_rating(rating, comment)
            st.success(t("rating_success"))
            st.balloons()
            st.rerun()
    
    with col2:
        # إحصائيات التقييمات
        avg_rating, total_ratings = get_average_rating()
        
        st.markdown(f"""
        <div class="metric-card">
            <h4>📊 {t('average_rating')}</h4>
            <h1 style="color: #f59e0b; text-align: center;">{avg_rating:.1f}/5</h1>
            <div style="text-align: center; font-size: 1.5rem; margin: 0.5rem 0;">
                {"⭐" * int(avg_rating) if avg_rating > 0 else ""}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <h4>📈 {t('total_ratings')}</h4>
            <h2 style="color: #667eea; text-align: center;">{total_ratings}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # عرض آخر التقييمات
        if not st.session_state.ratings_df.empty:
            st.markdown("**📝 آخر التقييمات:**")
            latest_ratings = st.session_state.ratings_df.tail(3)
            for _, rating in latest_ratings.iterrows():
                stars = "⭐" * rating["rating"] + "☆" * (5 - rating["rating"])
                st.markdown(f"""
                <div style='
                    background: rgba(255,255,255,0.1);
                    padding: 0.75rem;
                    border-radius: 10px;
                    margin: 0.5rem 0;
                    border-left: 4px solid #f59e0b;
                '>
                    <div style="display: flex; justify-content: between; align-items: center;">
                        <span>{stars}</span>
                        <small style="opacity: 0.7;">{rating['timestamp'].split()[0]}</small>
                    </div>
                    {f"<p style='margin: 0.5rem 0 0 0; opacity: 0.8;'>{rating['comment']}</p>" if pd.notna(rating['comment']) and rating['comment'].strip() else ""}
                </div>
                """, unsafe_allow_html=True)

# تشغيل التطبيق
if __name__ == "__main__":
    main()
