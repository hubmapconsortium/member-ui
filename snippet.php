// Register the metabox and fields.
add_action( 'cn_metabox', 'cn_register_custom_metabox_and_text_field' );
 
function cn_register_custom_metabox_and_text_field() {
    
	$role_atts = array(
        'title'    => 'Role in HuBMAP', // Change this to a name which applies to your project.
        'id'       => 'role', // Change this so it is unique to you project.
        'context'  => 'normal',
        'priority' => 'core',
        'fields'   => array(
            array(
                'name'       => 'role',     // Change this field name to something which applies to you project.
                'show_label' => TRUE,             // Whether or not to display the 'name'. Changing it to false will suppress the name.
                'id'         => 'role', // Change this so it is unique to you project. Each field id MUST be unique.
                'type'       => 'select',  // This is the field type being added.
                'options'    => array(
                    'administrative_assistant'   => 'Administrative Assistant',
                    'agreement_specialist'   => 'Agreement Specialist',
                    'co-investigator' => 'Co-investigator',
                    'compliance_officer'  => 'Complicance Officer',
                    'computer_scientist'  => 'Computer Scientist',
					'data_analysis_core' => 'Data Analysis Core',
					'data_architect' => 'Data Architect',
					'data_manager' => 'Data Manger',
					'data_scientist' => 'Data Scientist',
					'designer' => 'Designer',
					'external_program_consultant' => 'External Program Consultant',
					'graduate_student' => 'Graduate Student',
					'image_scientist' => 'Image Scientist',
					'informatics' => 'Informatics',
					'lead_software_developer' => 'Lead Software Developer',
					'ml_scientist' => 'ML scientist',
					'meeting_facilitator' => 'Meeting Facilitator',
					'network_support' => 'Network Support',
					'pi' => 'PI',
					'pi_contact' => 'PI (Contact)',
					'pathology_assessment' => 'Pathology Assessment',
					'postdoctoral_fellow' => 'Postdoctoral fellow',
					'program_coordinator' => 'Program Coordinator',
					'program_officer' => 'Program Officer',
					'program_manager' => 'Program Manager',
					'project_scientist' => 'Project Scientist',
					'researcher' => 'Researcher',
					'scientific_program_manager' => 'Scientific Program Manager',
					'software_developer' => 'Software Developer',
					'software_engineer' => 'Software Engineer',
					'system_support' => 'System Support',
					'team_leader' => 'Team Leader',
					'wg_member' => 'WG Member',
                    'website_developer' => 'Website Developer',
                    'other' => 'Other'
                ),
                'default'    => '', // This is the default selected option. Leave blank for none.
            ),
        ),
    );

    $other_role_atts = array(
		'title'    => 'Other Role',         // Change this to a name which applies to your project.
		'id'       => 'other_role',           // Change this so it is unique to you project.
		'context'  => 'normal',
		'priority' => 'core',
		'fields'   => array(
			array(
				'name'       => 'other role', // Change this field name to something which applies to you project.
				'show_label' => TRUE,         // Whether or not to display the 'name'. Changing it to false will suppress the name.
				'id'         => 'other_role',   // Change this so it is unique to you project. Each field id MUST be unique.
				'type'       => 'text',       // This is the field type being added.
				'size'       => 'regular',    // This can be changed to one of the following: 'small', 'regular', 'large'
			),
		),
	);
	
	$wg_atts = array(
		'title'    => 'What HuBMAP working group are you a member of?',         // Change this to a name which applies to your project.
		'id'       => 'working_group',           // Change this so it is unique to you project.
		'context'  => 'normal',
		'priority' => 'core',
		'fields'   => array(
			array(
				'name'       => 'working group', // Change this field name to something which applies to you project.
				'show_label' => TRUE,         // Whether or not to display the 'name'. Changing it to false will suppress the name.
				'id'         => 'working_group',   // Change this so it is unique to you project. Each field id MUST be unique.
				'type'       => 'checkboxgroup',       // This is the field type being added.
				'size'       => 'regular',    // This can be changed to one of the following: 'small', 'regular', 'large'
				'options'    => array(
                    'Communications & Engagement'   => 'Communications & Engagement',
                    'Data Science'   => 'Data Science',
                    'Policies' => 'Policies',
                    'Tissue, Technology & Data Collection'  => 'Tissue, Technology & Data Collection',
                    'Tools & Models'  => 'Tools & Models',
					'NA' => 'NA',
                ),
			),
		),
	);
	
	$ar_atts = array(
        'title'    => 'Which HuBMAP resources will you need to access?', // Change this to a name which applies to your project.
        'id'       => 'access_requests', // Change this so it is unique to you project.
        'context'  => 'normal',
        'priority' => 'core',
        'fields'   => array(
            array(
                'name'       => 'access request',     // Change this field name to something which applies to you project.
                'show_label' => TRUE,             // Whether or not to display the 'name'. Changing it to false will suppress the name.
                'id'         => 'access_requests', // Change this so it is unique to you project. Each field id MUST be unique.
                'type'       => 'checkboxgroup',  // This is the field type being added.
                'options'    => array(
                    'Sample Data Portal'   => 'Sample Data Portal',
                    'HuBMAP Data Portal'   => 'HuBMAP Data Portal',
                    'Collaboration Portal' => 'Collaboration Portal',
                    'HuBMAP Google Drive share'  => 'HuBMAP Google Drive share',
                    'HuBMAP GitHub repository'  => 'HuBMAP GitHub repository',
                    'HuBMAP Slack Workspace' => 'HuBMAP Slack Workspace',
                    'Edit My Component\'s Project Page' => 'Edit my component\'s project page'
                ),
                'default'    => '', // This is the default selected option. Leave blank for none.
            ),
        ),
    );
	
	$google_email_atts = array(
		'title'    => 'What email address is linked to your preferred Google account?',         // Change this to a name which applies to your project.
		'id'       => 'google_email',           // Change this so it is unique to you project.
		'context'  => 'normal',
		'priority' => 'core',
		'fields'   => array(
			array(
				'name'       => 'google email', // Change this field name to something which applies to you project.
				'show_label' => TRUE,         // Whether or not to display the 'name'. Changing it to false will suppress the name.
				'id'         => 'google_email',   // Change this so it is unique to you project. Each field id MUST be unique.
				'type'       => 'text',       // This is the field type being added.
				'size'       => 'regular',    // This can be changed to one of the following: 'small', 'regular', 'large'
			),
		),
    );
    
    $github_username_atts = array(
		'title'    => 'What is your GitHub username?',         // Change this to a name which applies to your project.
		'id'       => 'github_username',           // Change this so it is unique to you project.
		'context'  => 'normal',
		'priority' => 'core',
		'fields'   => array(
			array(
				'name'       => 'github username', // Change this field name to something which applies to you project.
				'show_label' => TRUE,         // Whether or not to display the 'name'. Changing it to false will suppress the name.
				'id'         => 'github_username',   // Change this so it is unique to you project. Each field id MUST be unique.
				'type'       => 'text',       // This is the field type being added.
				'size'       => 'regular',    // This can be changed to one of the following: 'small', 'regular', 'large'
			),
		),
    );
    
    $slack_username_atts = array(
		'title'    => 'What is your Slack username?',         // Change this to a name which applies to your project.
		'id'       => 'slack_username',           // Change this so it is unique to you project.
		'context'  => 'normal',
		'priority' => 'core',
		'fields'   => array(
			array(
				'name'       => 'slack username', // Change this field name to something which applies to you project.
				'show_label' => TRUE,         // Whether or not to display the 'name'. Changing it to false will suppress the name.
				'id'         => 'slack_username',   // Change this so it is unique to you project. Each field id MUST be unique.
				'type'       => 'text',       // This is the field type being added.
				'size'       => 'regular',    // This can be changed to one of the following: 'small', 'regular', 'large'
			),
		),
	);
	
	$website_atts = array(
		'title'    => 'Personal Website',         // Change this to a name which applies to your project.
		'id'       => 'website',           // Change this so it is unique to you project.
		'context'  => 'normal',
		'priority' => 'core',
		'fields'   => array(
			array(
				'name'       => 'Personal website', // Change this field name to something which applies to you project.
				'show_label' => TRUE,         // Whether or not to display the 'name'. Changing it to false will suppress the name.
				'id'         => 'website',   // Change this so it is unique to you project. Each field id MUST be unique.
				'type'       => 'text',       // This is the field type being added.
				'size'       => 'regular',    // This can be changed to one of the following: 'small', 'regular', 'large'
			),
		),
	);
	
	$biosketch_atts = array(
		'title'    => 'Biosketch',         // Change this to a name which applies to your project.
		'id'       => 'biosketch',           // Change this so it is unique to you project.
		'context'  => 'normal',
		'priority' => 'core',
		'fields'   => array(
			array(
				'name'       => 'Biosketch', // Change this field name to something which applies to you project.
				'show_label' => TRUE,         // Whether or not to display the 'name'. Changing it to false will suppress the name.
				'id'         => 'biosketch',   // Change this so it is unique to you project. Each field id MUST be unique.
				'type'       => 'text',       // This is the field type being added.
				'size'       => 'regular',    // This can be changed to one of the following: 'small', 'regular', 'large'
			),
		),
	);
	
	$expertise_atts = array(
		'title'    => 'Area of Expertise',         // Change this to a name which applies to your project.
		'id'       => 'expertise',           // Change this so it is unique to you project.
		'context'  => 'normal',
		'priority' => 'core',
		'fields'   => array(
			array(
				'name'       => 'Area of Expertise', // Change this field name to something which applies to you project.
				'show_label' => TRUE,         // Whether or not to display the 'name'. Changing it to false will suppress the name.
				'id'         => 'expertise',   // Change this so it is unique to you project. Each field id MUST be unique.
				'type'       => 'text',       // This is the field type being added.
				'size'       => 'regular',    // This can be changed to one of the following: 'small', 'regular', 'large'
			),
		),
	);
	
	$orcid_atts = array(
		'title'    => 'What is your ORCID ID?',         // Change this to a name which applies to your project.
		'id'       => 'orcid',           // Change this so it is unique to you project.
		'context'  => 'normal',
		'priority' => 'core',
		'fields'   => array(
			array(
				'name'       => 'ORCID ID', // Change this field name to something which applies to you project.
				'show_label' => TRUE,         // Whether or not to display the 'name'. Changing it to false will suppress the name.
				'id'         => 'orcid',   // Change this so it is unique to you project. Each field id MUST be unique.
				'type'       => 'text',       // This is the field type being added.
				'size'       => 'regular',    // This can be changed to one of the following: 'small', 'regular', 'large'
			),
		),
	);
	
	$pm_atts = array(
		'title'    => 'Is there a project manager who should be copied on all communications to you?',         // Change this to a name which applies to your project.
		'id'       => 'pm',           // Change this so it is unique to you project.
		'context'  => 'normal',
		'priority' => 'core',
		'fields'   => array(
			array(
				'name'       => 'pm', // Change this field name to something which applies to you project.
				'show_label' => TRUE,         // Whether or not to display the 'name'. Changing it to false will suppress the name.
				'id'         => 'pm',   // Change this so it is unique to you project. Each field id MUST be unique.
				'type'       => 'radio',       // This is the field type being added.
				'size'       => 'regular',    // This can be changed to one of the following: 'small', 'regular', 'large'
				'options'    => array(
                    'yes'   => 'Yes',
                    'no'   => 'No',
                ),
			),
		),
    );
    
    $pm_name_atts = array(
		'title'    => 'Project Manager\'s name',         // Change this to a name which applies to your project.
		'id'       => 'pm_name',           // Change this so it is unique to you project.
		'context'  => 'normal',
		'priority' => 'core',
		'fields'   => array(
			array(
				'name'       => 'pm name', // Change this field name to something which applies to you project.
				'show_label' => TRUE,         // Whether or not to display the 'name'. Changing it to false will suppress the name.
				'id'         => 'pm_name',   // Change this so it is unique to you project. Each field id MUST be unique.
				'type'       => 'text',       // This is the field type being added.
				'size'       => 'regular',    // This can be changed to one of the following: 'small', 'regular', 'large'
			),
		),
	);
	
	$pm_email_atts = array(
		'title'    => 'Project Manager\'s email',         // Change this to a name which applies to your project.
		'id'       => 'pm_email',           // Change this so it is unique to you project.
		'context'  => 'normal',
		'priority' => 'core',
		'fields'   => array(
			array(
				'name'       => 'pm email', // Change this field name to something which applies to you project.
				'show_label' => TRUE,         // Whether or not to display the 'name'. Changing it to false will suppress the name.
				'id'         => 'pm_email',   // Change this so it is unique to you project. Each field id MUST be unique.
				'type'       => 'text',       // This is the field type being added.
				'size'       => 'regular',    // This can be changed to one of the following: 'small', 'regular', 'large'
			),
		),
	);
 
    cnMetaboxAPI::add( $role_atts );
    cnMetaboxAPI::add( $other_role_atts);
	cnMetaboxAPI::add( $wg_atts );
    cnMetaboxAPI::add( $ar_atts );
    cnMetaboxAPI::add( $google_email_atts);
    cnMetaboxAPI::add( $github_username_atts);
    cnMetaboxAPI::add( $slack_username_atts);
	cnMetaboxAPI::add( $website_atts );
	cnMetaboxAPI::add( $biosketch_atts );
	cnMetaboxAPI::add( $expertise_atts );
	cnMetaboxAPI::add( $orcid_atts );
    cnMetaboxAPI::add( $pm_atts );
    cnMetaboxAPI::add( $pm_name_atts );
	cnMetaboxAPI::add( $pm_email_atts );
}

// Register the custom fields CSV Import mapping options and processing callback.
add_filter( 'cncsv_map_import_fields', 'cncsv_header_name' );
add_action( 'cncsv_import_fields', 'cncsv_process_import', 10, 3 );
 
function cncsv_header_name( $fields ) {
 
	// The field_id should match exactly the field id used when registering the custom field.
	$fields['working_group'] = 'Working Group';
 
	return $fields;
}
 
function cncsv_process_import( $id, $row, $entry ) {
 
	$data = array();
 
	if ( $entry->arrayKeyExists( $row, 'working_group' ) ) {
 
		// The field_id should match exactly the field id used when registering the custom field.
		$value = $entry->arrayPull( $row, 'working_group', '' );
		$value = cnFormatting::maybeJSONdecode( stripslashes( $value ) );
 
		$data[] = array(
			'key'   => 'working_group',
			'value' => $value,
		);
	}
 
	if ( 0 < count( $data ) ) {
 
		cnEntry_Action::meta( 'update', $id, $data );
	}
}